--- libmamba/src/core/virtual_packages.cpp.orig	2024-12-11 11:32:41 UTC
+++ libmamba/src/core/virtual_packages.cpp
@@ -10,6 +10,7 @@
 #include "mamba/util/build.hpp"
 #include "mamba/util/environment.hpp"
 #include "mamba/util/os_linux.hpp"
+#include "mamba/util/os_freebsd.hpp"
 #include "mamba/util/os_osx.hpp"
 #include "mamba/util/os_win.hpp"
 #include "mamba/util/string.hpp"
@@ -342,6 +343,15 @@ namespace mamba
             return util::osx_version();
         }
 
+        [[nodiscard]] auto overridable_freebsd_version() -> tl::expected<std::string, util::OSError>
+        {
+            if (auto override_version = util::get_env("CONDA_OVERRIDE_FREEBSD"))
+            {
+                return { std::move(override_version).value() };
+            }
+            return util::freebsd_version();
+        }
+
         [[nodiscard]] auto overridable_windows_version() -> tl::expected<std::string, util::OSError>
         {
             if (auto override_version = util::get_env("CONDA_OVERRIDE_WIN"))
@@ -458,6 +468,32 @@ namespace mamba
                             LOG_DEBUG << err.message;
                         }
                     );
+            }
+
+            if (os == "freebsd")
+            {
+                res.push_back(make_virtual_package("__unix", platform));
+
+                overridable_freebsd_version()
+                    .transform(
+                        [&](std::string&& version)
+                        {
+                            res.push_back(
+                                make_virtual_package("__freebsd", platform, std::move(version))
+                            );
+                        }
+                    )
+                    .or_else(
+                        [&](util::OSError err)
+                        {
+                            res.push_back(make_virtual_package("__freebsd", platform, "0"));
+                            LOG_WARNING
+                                << "FreeBSD version not found, defaulting virtual package version to 0."
+                                   " Try setting CONDA_OVERRIDE_FREEBSD environment variable to the"
+                                   " desired version.";
+                            LOG_DEBUG << err.message;
+                        }
+                    );
             }
 
             res.push_back(make_virtual_package("__archspec", platform, "1", get_archspec(arch)));
