#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import urllib.request
import argparse

# Configuration
FBSD_VERSION = "14.4"
TARGET = f"x86_64-pc-freebsd{FBSD_VERSION}"
SYSROOT_DIR = os.path.abspath(f"./sysroot/{TARGET}")
RATTLER_BUILD_VERSION = "0.64.1"
RATTLER_BUILD_URL = f"https://github.com/prefix-dev/rattler-build/releases/download/v{RATTLER_BUILD_VERSION}/rattler-build-x86_64-unknown-linux-musl"
BIN_DIR = os.path.abspath("./.bin")
RATTLER_BUILD_PATH = os.path.join(BIN_DIR, "rattler-build")
CONDA_BLD_DIR = os.path.abspath("./conda-bld")
CHANNEL_DIR = os.path.abspath("./conda-channel")
RECIPES_DIR = os.path.abspath("./recipes")

RECIPES = [
    "zlib",
    "openssl",
    "libffi",
    "bzip2",
    "xz",
    "readline",
    "sqlite",
    "python",
    "openblas",
    "numpy",
    "pandas",
    "fmt",
    "reproc",
    "yaml-cpp",
    "simdjson",
    "libsolv",
    "libmamba",
    "micromamba"
]

def check_host_dependencies():
    """Verify that cross compilation tools are installed on the host."""
    print("=== Checking Host Dependencies ===")
    required_commands = ["clang", "lld", "llvm-ar", "cmake", "ninja", "tar", "unzip", "zstd"]
    missing = []
    for cmd in required_commands:
        if shutil.which(cmd) is None:
            missing.append(cmd)
    
    if missing:
        print(f"Error: Missing compiler tools: {', '.join(missing)}")
        print("Please install them using: pkg install -y llvm clang lld cmake ninja zstd unzip")
        sys.exit(1)
    print("Host toolchain dependencies: OK")

def install_rattler_build():
    """Download and configure rattler-build tool."""
    if os.path.exists(RATTLER_BUILD_PATH):
        print(f"rattler-build already installed at {RATTLER_BUILD_PATH}")
        return

    print("=== Installing rattler-build ===")
    os.makedirs(BIN_DIR, exist_ok=True)
    print(f"Downloading from {RATTLER_BUILD_URL}...")
    try:
        urllib.request.urlretrieve(RATTLER_BUILD_URL, RATTLER_BUILD_PATH)
        os.chmod(RATTLER_BUILD_PATH, 0o755)
        print("rattler-build installation successful.")
    except Exception as e:
        print(f"Failed to download rattler-build: {e}")
        sys.exit(1)

def setup_sysroot():
    """Set up FreeBSD sysroot locally under the workspace."""
    print("=== Checking FreeBSD Sysroot ===")
    if os.path.exists(os.path.join(SYSROOT_DIR, "usr/include/stdio.h")):
        print(f"Sysroot already configured at {SYSROOT_DIR}")
        return

    print(f"Sysroot not found at {SYSROOT_DIR}.")
    print(f"Downloading and extracting FreeBSD {FBSD_VERSION} base system locally...")
    
    base_url = f"https://download.freebsd.org/releases/amd64/{FBSD_VERSION}-RELEASE/base.txz"
    txz_path = "./base.txz"
    
    if not os.path.exists(txz_path):
        print(f"Downloading base.txz from {base_url}...")
        try:
            urllib.request.urlretrieve(base_url, txz_path)
            print("Download finished.")
        except Exception as e:
            print(f"Failed to download base.txz: {e}")
            sys.exit(1)
            
    print(f"Extracting sysroot to {SYSROOT_DIR}...")
    os.makedirs(SYSROOT_DIR, exist_ok=True)
    
    tar_cmd = [
        "tar", "-C", SYSROOT_DIR, "-xf", txz_path,
        "./usr/include", "./usr/lib", "./usr/libdata", "./lib", "./libexec"
    ]
    print(f"Running: {' '.join(tar_cmd)}")
    subprocess.run(tar_cmd, check=True)
    
    if os.path.exists(txz_path):
        os.remove(txz_path)
        
    # Verify
    if os.path.exists(os.path.join(SYSROOT_DIR, "usr/include/stdio.h")):
        print("Sysroot setup complete and verified (No sudo used!).")
    else:
        print("Error: Sysroot verification failed.")
        sys.exit(1)

def build_packages():
    """Build all recipes in correct order."""
    print("=== Building FreeBSD Conda Packages ===")
    os.makedirs(CONDA_BLD_DIR, exist_ok=True)
    
    for recipe in RECIPES:
        recipe_path = os.path.join(RECIPES_DIR, recipe, "recipe.yaml")
        if not os.path.exists(recipe_path):
            print(f"Error: Recipe not found at {recipe_path}")
            sys.exit(1)
            
        print(f"\n--- Building {recipe} ---")
        
        # Read the recipe and temporarily patch the sysroot path directly in the recipe
        # to bypass rattler-build environment scrubbing
        with open(recipe_path, "r") as f:
            original_content = f.read()
            
        patched_content = original_content.replace(
            'sysroot: ${{ env.SYSROOT | default("/opt/freebsd-sysroot/x86_64-pc-freebsd14.4") }}',
            f'sysroot: "{SYSROOT_DIR}"'
        )
        # Also handle any legacy placeholder if not updated
        patched_content = patched_content.replace(
            'sysroot: "/opt/freebsd-sysroot/x86_64-pc-freebsd14.4"',
            f'sysroot: "{SYSROOT_DIR}"'
        )
        
        with open(recipe_path, "w") as f:
            f.write(patched_content)
            
        build_cmd = [
            RATTLER_BUILD_PATH, "build",
            "--recipe", recipe_path,
            "--output-dir", CONDA_BLD_DIR,
            "--target-platform", "freebsd-64",
            "--compression-threads", "1",
            "--skip-existing", "local"
        ]
        
        # If we have local channel packages built, add local build dir as channel to resolve dependencies
        if os.path.exists(CONDA_BLD_DIR):
            index_channel()
            build_cmd.extend(["-c", f"file://{CHANNEL_DIR}", "-c", "conda-forge"])
            
        print(f"Running: {' '.join(build_cmd)}")
        result = subprocess.run(build_cmd)
        
        # Restore original recipe content
        with open(recipe_path, "w") as f:
            f.write(original_content)
            
        if result.returncode != 0:
            print(f"Error: Failed to build {recipe}")
            sys.exit(1)
            
        print(f"Successfully built {recipe}")

def index_channel():
    """Move packages to the conda-channel and index it."""
    print("=== Indexing Conda Channel ===")
    os.makedirs(os.path.join(CHANNEL_DIR, "freebsd-64"), exist_ok=True)
    
    # Find all built conda packages and copy them to freebsd-64 subdirectory
    packages_copied = 0
    for root, dirs, files in os.walk(CONDA_BLD_DIR):
        for file in files:
            if file.endswith(".conda") or file.endswith(".tar.bz2"):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(CHANNEL_DIR, "freebsd-64", file)
                if not os.path.exists(dest_path) or os.path.getmtime(src_path) > os.path.getmtime(dest_path):
                    shutil.copy2(src_path, dest_path)
                    packages_copied += 1
                    
    if packages_copied > 0:
        print(f"Copied {packages_copied} new packages to {CHANNEL_DIR}/freebsd-64/")
        
    # Index the channel using conda-index (inside a virtualenv if not installed)
    if shutil.which("conda-index") is None:
        print("conda-index not found in PATH. Creating temporary venv to run conda-index...")
        venv_dir = os.path.join(BIN_DIR, "index_venv")
        if not os.path.exists(venv_dir):
            subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
            pip_bin = os.path.join(venv_dir, "bin", "pip")
            subprocess.run([pip_bin, "install", "conda-index"], check=True)
        
        index_bin = os.path.join(venv_dir, "bin", "conda-index")
        subprocess.run([index_bin, CHANNEL_DIR], check=True)
    else:
        subprocess.run(["conda-index", CHANNEL_DIR], check=True)
        
    print(f"Conda channel indexed at {CHANNEL_DIR}")

def extract_micromamba_binary():
    """Extract micromamba binary for standalone execution."""
    print("=== Extracting Standalone Micromamba Binary ===")
    freebsd_pkg_dir = os.path.join(CHANNEL_DIR, "freebsd-64")
    if not os.path.exists(freebsd_pkg_dir):
        print("No freebsd-64 channel directory found.")
        return
    micromamba_pkgs = [f for f in os.listdir(freebsd_pkg_dir) if f.startswith("micromamba") and f.endswith(".conda")]
    
    if not micromamba_pkgs:
        print("Error: No micromamba package found in the channel. Build it first.")
        return
        
    pkg_file = os.path.join(freebsd_pkg_dir, sorted(micromamba_pkgs)[-1])
    out_dir = os.path.abspath("./standalone")
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"Extracting {pkg_file} to {out_dir}...")
    
    try:
        temp_extract = os.path.join(out_dir, "temp_extract")
        os.makedirs(temp_extract, exist_ok=True)
        
        subprocess.run(["unzip", "-o", "-q", pkg_file, "-d", temp_extract], check=True)
        
        pkg_tar_zst = [f for f in os.listdir(temp_extract) if f.startswith("pkg-") and f.endswith(".tar.zst")]
        if not pkg_tar_zst:
            print("Error: Could not find pkg-*.tar.zst in the .conda archive.")
            return
            
        tar_zst_path = os.path.join(temp_extract, pkg_tar_zst[0])
        
        zstd_cmd = f"zstd -d -c {tar_zst_path} | tar -C {out_dir} -xf - --wildcards '*/bin/micromamba'"
        subprocess.run(zstd_cmd, shell=True, check=True)
        
        binary_path = None
        for root, dirs, files in os.walk(out_dir):
            if "micromamba" in files and root != out_dir:
                found_path = os.path.join(root, "micromamba")
                dest_path = os.path.join(out_dir, "micromamba-freebsd")
                shutil.copy2(found_path, dest_path)
                os.chmod(dest_path, 0o755)
                binary_path = dest_path
                break
                
        shutil.rmtree(temp_extract)
        shutil.rmtree(os.path.join(out_dir, "bin"), ignore_errors=True)
        
        if binary_path:
            print(f"Micromamba FreeBSD binary successfully extracted to: {binary_path}")
        else:
            print("Error: Could not find extracted micromamba binary.")
    except Exception as e:
        print(f"Failed to extract micromamba: {e}")

def serve_channel(port=8000):
    """Serve the local conda-channel over HTTP."""
    print(f"=== Serving Conda Channel on Port {port} ===")
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
        
    print(f"\n  URL: http://{IP}:{port}")
    print(f"\nExample installation command:")
    print(f"  conda install -c http://{IP}:{port} -c conda-forge fmt reproc libsolv")
    print("\nPress Ctrl+C to stop the server.")
    
    import http.server
    import socketserver
    
    Handler = http.server.SimpleHTTPRequestHandler
    os.chdir(CHANNEL_DIR)
    
    class TCPServerReuseAddr(socketserver.TCPServer):
        allow_reuse_address = True
        
    with TCPServerReuseAddr(("", port), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

def main():
    parser = argparse.ArgumentParser(description="Farm and index FreeBSD-64 Conda Packages")
    parser.add_argument("action", choices=["all", "setup", "build", "index", "extract", "serve"], 
                        default="all", nargs="?",
                        help="Action to perform: \n"
                             "setup: Check host tools and setup FreeBSD sysroot\n"
                             "build: Build all recipes\n"
                             "index: Copy packages and index conda channel\n"
                             "extract: Extract the built micromamba FreeBSD binary\n"
                             "serve: Serve local conda channel over HTTP\n"
                             "all: Run setup, build, index, and extract")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve conda channel on (default: 8000)")
    
    args = parser.parse_args()
    
    if args.action == "setup":
        check_host_dependencies()
        install_rattler_build()
        setup_sysroot()
    elif args.action == "build":
        build_packages()
    elif args.action == "index":
        index_channel()
    elif args.action == "extract":
        extract_micromamba_binary()
    elif args.action == "serve":
        serve_channel(args.port)
    elif args.action == "all":
        check_host_dependencies()
        install_rattler_build()
        setup_sysroot()
        build_packages()
        index_channel()
        extract_micromamba_binary()
        print("\n=== Success! ===")
        print("All packages built, indexed, and micromamba binary extracted.")
        print(f"Run 'python3 farm.py serve --port {args.port}' to start serving the channel.")

if __name__ == "__main__":
    main()
