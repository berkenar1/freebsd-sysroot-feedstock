--- /dev/null	2026-05-05 00:00:00 UTC
+++ libmamba/src/util/os_freebsd.cpp
@@ -0,0 +1,29 @@
+// Copyright (c) 2024, QuantStack and Mamba Contributors
+//
+// Distributed under the terms of the BSD 3-Clause License.
+//
+// The full license is in the file LICENSE, distributed with this software.
+
+#include <fmt/format.h>
+
+#include "mamba/util/os_freebsd.hpp"
+#include "mamba/util/os_unix.hpp"
+
+namespace mamba::util
+{
+    auto freebsd_version() -> tl::expected<std::string, OSError>
+    {
+        return unix_name_version().and_then(
+            [](auto&& name_version) -> tl::expected<std::string, OSError>
+            {
+                if (name_version.first != "FreeBSD")
+                {
+                    return tl::make_unexpected(OSError{
+                        fmt::format(R"(OS "{}" is not FreeBSD)", name_version.first),
+                    });
+                }
+                return { std::forward<decltype(name_version)>(name_version).second };
+            }
+        );
+    }
+}
