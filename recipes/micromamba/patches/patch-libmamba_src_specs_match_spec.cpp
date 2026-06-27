--- libmamba/src/specs/match_spec.cpp.orig	2026-05-05 00:00:00 UTC
+++ libmamba/src/specs/match_spec.cpp
@@ -456,23 +456,26 @@
             }
 
             pos = str.find_last_of('=');
-            const char d = str[pos - 1];
-
-            if (d == '=' || d == '!' || d == '|' || d == ',' || d == '<' || d == '>' || d == '~')
+            if (pos != str.npos && pos > 0)
             {
-                // Find the position of the first non-space character after operator
-                const auto version_start = str.find_first_not_of(' ', pos + 1);
-                const auto space_start = str.find_first_of(' ', version_start);
-                // Find the position of the first non-space character after version
-                const auto build_start = str.find_first_not_of(' ', space_start);
+                const char d = str[pos - 1];
 
-                // If another str is present after some space => build
-                if ((build_start != str.npos) && (version_start != build_start))
+                if (d == '=' || d == '!' || d == '|' || d == ',' || d == '<' || d == '>' || d == '~')
                 {
-                    return { util::strip(str.substr(0, build_start)), str.substr(build_start) };
+                    // Find the position of the first non-space character after operator
+                    const auto version_start = str.find_first_not_of(' ', pos + 1);
+                    const auto space_start = str.find_first_of(' ', version_start);
+                    // Find the position of the first non-space character after version
+                    const auto build_start = str.find_first_not_of(' ', space_start);
+
+                    // If another str is present after some space => build
+                    if ((build_start != str.npos) && (version_start != build_start))
+                    {
+                        return { util::strip(str.substr(0, build_start)), str.substr(build_start) };
+                    }
+                    // Otherwise no build is present after the version
+                    return { str, {} };
                 }
-                // Otherwise no build is present after the version
-                return { str, {} };
             }
 
             if (pos == str.npos)
