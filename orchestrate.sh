#!/usr/bin/env bash

# Exit immediately if any command in a non-interactive pipeline fails
set -euo pipefail

# ANSI color codes for premium terminal UI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Config
FARM_SCRIPT="farm.py"
LOG_FILE="orchestration.log"

# Print banner
print_banner() {
    echo -e "${CYAN}================================================================${NC}"
    echo -e "${CYAN}${BOLD}     FreeBSD-64 Conda Sysroot & Package Orchestrator            ${NC}"
    echo -e "${CYAN}================================================================${NC}"
}

# Logger helper
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    if ! command -v python3 &>/dev/null; then
        log_error "python3 is not installed or not in PATH."
        exit 1
    fi
}

# Run a farm action with real-time output and logging
run_action() {
    local action="$1"
    local desc="$2"
    
    echo -e "\n${BLUE}=== Running step: ${BOLD}${desc}${NC} (${action}) ==="
    log_info "Logging output to ${LOG_FILE}"
    
    # We use tee to write to stdout and log file simultaneously
    # Note: Using python3 -u ensures stdout is unbuffered so tee works in real time
    if python3 -u "${FARM_SCRIPT}" "${action}" 2>&1 | tee -a "${LOG_FILE}"; then
        log_info "Step '${desc}' completed successfully!"
    else
        log_error "Step '${desc}' failed! Please check ${LOG_FILE} for details."
        if [ "$action" = "build" ]; then
            print_build_summary "true"
        fi
        exit 1
    fi
}

# Print a nice summary of built, failed, and pending packages
print_build_summary() {
    local is_failure="$1"
    
    local recipes=(
        "sysroot_freebsd-64" "clang_freebsd-64" "clangxx_freebsd-64"
        "zlib" "openssl" "libffi" "bzip2" "xz" "readline" "sqlite"
        "python" "fmt" "reproc" "yaml-cpp" "simdjson" "libsolv" "libmamba"
        "micromamba" "openblas" "numpy" "pandas" "scipy" "markupsafe" "pyyaml"
        "cffi" "psutil" "frozenlist" "multidict" "propcache" "yarl" "wrapt"
        "regex" "greenlet" "sqlalchemy" "tornado" "cryptography" "protobuf" "pydantic-core"
        "aiohttp" "uvicorn" "pillow" "rpds-py" "grpcio" "pyarrow" "lxml"
        "matplotlib" "scikit-learn" "tokenizers" "tiktoken" "pyzmq" "numba" "polars"
        "duckdb" "xgboost" "h5py" "statsmodels" "scikit-image" "lightgbm" "shap"
        "kaleido" "prophet" "catboost" "gensim" "cvxpy" "wordcloud" "pymc"
        "cython" "msgpack" "ujson" "simplejson" "kiwisolver" "unicodedata2"
        "brotli" "lz4" "zstandard" "xxhash" "bitarray" "pyrsistent" "lru-dict"
        "gevent" "websockets" "pycurl" "pyodbc" "psycopg2" "pyreadstat" "bottleneck"
        "numexpr" "pywavelets" "astropy" "netcdf4" "pyproj" "shapely" "fiona"
        "rasterio" "fastparquet" "thrift" "coverage" "fastcache" "immutables" "crc32c"
        "bcrypt" "pynacl" "ciso8601" "netifaces" "pycryptodome"
    )
    
    local built=()
    local failed=""
    local pending=()
    
    local found_failure=0
    for r in "${recipes[@]}"; do
        if ls conda-channel/freebsd-64/${r}-* &>/dev/null || ls conda-channel/noarch/${r}-* &>/dev/null; then
            built+=("$r")
        else
            if [ $found_failure -eq 0 ]; then
                failed="$r"
                found_failure=1
            else
                pending+=("$r")
            fi
        fi
    done
    
    echo -e "\n${CYAN}${BOLD}================ Build Summary ================${NC}"
    
    # 1. Successfully completed
    if [ ${#built[@]} -gt 0 ]; then
        echo -e "${GREEN}${BOLD}✓ Successfully Completed (${#built[@]}):${NC}"
        for b in "${built[@]}"; do
            echo -e "  - $b"
        done
    fi
    
    # 2. Failed package (only if this was called due to a failure)
    if [ "$is_failure" = "true" ] && [ -n "$failed" ]; then
        echo -e "\n${RED}${BOLD}✗ Failed Package:${NC}"
        echo -e "  - ${BOLD}$failed${NC} (Check ${LOG_FILE} for compile errors)"
    fi
    
    # 3. Not completed
    if [ ${#pending[@]} -gt 0 ]; then
        if [ "$is_failure" = "true" ]; then
            echo -e "\n${YELLOW}${BOLD}⚠ Not Completed / Skipped (${#pending[@]}):${NC}"
        else
            echo -e "\n${YELLOW}${BOLD}⚠ Pending / Skipped (${#pending[@]}):${NC}"
        fi
        for p in "${pending[@]}"; do
            echo -e "  - $p"
        done
    fi
    echo -e "${CYAN}${BOLD}===============================================${NC}\n"
}

# Check build status of target list
check_status() {
    echo -e "\n${CYAN}${BOLD}--- Target Package Build Status ---${NC}"
    
    # List of configured recipes (extracted from farm.py)
    local recipes=(
        "sysroot_freebsd-64" "clang_freebsd-64" "clangxx_freebsd-64"
        "zlib" "openssl" "libffi" "bzip2" "xz" "readline" "sqlite"
        "python" "fmt" "reproc" "yaml-cpp" "simdjson" "libsolv" "libmamba"
        "micromamba" "openblas" "numpy" "pandas" "scipy" "markupsafe" "pyyaml"
        "cffi" "psutil" "frozenlist" "multidict" "propcache" "yarl" "wrapt"
        "regex" "greenlet" "sqlalchemy" "tornado" "cryptography" "protobuf" "pydantic-core"
        "aiohttp" "uvicorn" "pillow" "rpds-py" "grpcio" "pyarrow" "lxml"
        "matplotlib" "scikit-learn" "tokenizers" "tiktoken" "pyzmq" "numba" "polars"
        "duckdb" "xgboost" "h5py" "statsmodels" "scikit-image" "lightgbm" "shap"
        "kaleido" "prophet" "catboost" "gensim" "cvxpy" "wordcloud" "pymc"
        "cython" "msgpack" "ujson" "simplejson" "kiwisolver" "unicodedata2"
        "brotli" "lz4" "zstandard" "xxhash" "bitarray" "pyrsistent" "lru-dict"
        "gevent" "websockets" "pycurl" "pyodbc" "psycopg2" "pyreadstat" "bottleneck"
        "numexpr" "pywavelets" "astropy" "netcdf4" "pyproj" "shapely" "fiona"
        "rasterio" "fastparquet" "thrift" "coverage" "fastcache" "immutables" "crc32c"
        "bcrypt" "pynacl" "ciso8601" "netifaces" "pycryptodome"
    )
    
    local built_count=0
    local total_count=${#recipes[@]}
    
    for r in "${recipes[@]}"; do
        # Search for package file starting with package name followed by dash in freebsd-64 or noarch
        if ls conda-channel/freebsd-64/${r}-* &>/dev/null || ls conda-channel/noarch/${r}-* &>/dev/null; then
            echo -e "  ${GREEN}[✓] Built${NC}   - ${BOLD}${r}${NC}"
            built_count=$((built_count + 1))
        else
            echo -e "  ${RED}[ ] Pending${NC} - ${r}"
        fi
    done
    
    echo -e "\nProgress: ${BOLD}${built_count}/${total_count}${NC} packages built."
}

# Interactive Menu
show_menu() {
    while true; do
        print_banner
        echo -e "Please select an action to perform:"
        echo -e "  ${BOLD}1)${NC} Run Full Pipeline (Setup -> Build -> Index -> Extract)"
        echo -e "  ${BOLD}2)${NC} Setup Environment (Host deps & local FreeBSD sysroot)"
        echo -e "  ${BOLD}3)${NC} Build Packages (Compile recipes targeting freebsd-64)"
        echo -e "  ${BOLD}4)${NC} Index Conda Channel (Create repodata/channel metadata)"
        echo -e "  ${BOLD}5)${NC} Extract Micromamba (Get the standalone FreeBSD binary)"
        echo -e "  ${BOLD}6)${NC} Serve Channel (Start HTTP server for local conda-channel)"
        echo -e "  ${BOLD}7)${NC} View Package Build Status checklist"
        echo -e "  ${BOLD}8)${NC} Exit"
        echo
        read -rp "Enter choice [1-8]: " choice
        
        case $choice in
            1)
                run_pipeline
                break
                ;;
            2)
                run_action "setup" "Setup Environment & Sysroot"
                ;;
            3)
                run_action "build" "Build Recipes"
                print_build_summary "false"
                ;;
            4)
                run_action "index" "Index Local Conda Channel"
                ;;
            5)
                run_action "extract" "Extract Standalone Micromamba"
                ;;
            6)
                echo -e "\n${BLUE}=== Serving Conda Channel ===${NC}"
                python3 "${FARM_SCRIPT}" "serve"
                ;;
            7)
                check_status
                ;;
            8)
                echo "Exiting."
                exit 0
                ;;
            *)
                log_warn "Invalid option. Please choose between 1 and 8."
                ;;
        esac
        echo -e "\nPress Enter to return to the menu..."
        read -r
    done
}

# Run the complete sequential pipeline
run_pipeline() {
    echo -e "\n${BOLD}${CYAN}>>> Starting Full Pipeline Orchestration <<<${NC}"
    echo "Started at $(date)" >> "${LOG_FILE}"
    
    run_action "setup" "Setup Environment & Sysroot"
    run_action "build" "Build Recipes"
    run_action "index" "Index Local Conda Channel"
    run_action "extract" "Extract Standalone Micromamba"
    
    echo -e "\n${BOLD}${GREEN}>>> Pipeline Completed Successfully! <<<${NC}"
    check_status
}

# Main Execution Flow
check_python

# If arguments are passed, run without the interactive menu
if [ $# -gt 0 ]; then
    action="$1"
    case $action in
        setup)
            run_action "setup" "Setup Environment & Sysroot"
            ;;
        build)
            run_action "build" "Build Recipes"
            print_build_summary "false"
            ;;
        index)
            run_action "index" "Index Local Conda Channel"
            ;;
        extract)
            run_action "extract" "Extract Standalone Micromamba"
            ;;
        serve)
            python3 "${FARM_SCRIPT}" "serve"
            ;;
        status)
            check_status
            ;;
        all)
            run_pipeline
            ;;
        help|-h|--help)
            echo "Usage: $0 [action]"
            echo "Actions:"
            echo "  setup   - Set up dependencies and target sysroot"
            echo "  build   - Compile all configured recipes"
            echo "  index   - Copy and index conda packages in the channel"
            echo "  extract - Extract the micromamba FreeBSD binary"
            echo "  serve   - Serve local channel over HTTP"
            echo "  status  - Show checklist of build status for target packages"
            echo "  all     - Run setup, build, index, and extract sequentially"
            echo "  (none)  - Launch interactive text menu"
            ;;
        *)
            log_error "Unknown action: $action"
            echo "Run '$0 --help' for usage instructions."
            exit 1
            ;;
    esac
else
    show_menu
fi
