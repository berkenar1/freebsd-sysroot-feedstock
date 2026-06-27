--- libmamba/include/mamba/specs/platform.hpp.orig	2026-05-05 00:00:00 UTC
+++ libmamba/include/mamba/specs/platform.hpp
@@ -32,6 +32,8 @@ namespace mamba::specs
         win_32,
         win_64,
         win_arm64,
+        freebsd_32,
+        freebsd_64,
         zos_z,
 
         // For reflexion purposes only
@@ -176,6 +178,10 @@ namespace mamba::specs
                 return "win-64";
             case KnownPlatform::win_arm64:
                 return "win-arm64";
+            case KnownPlatform::freebsd_32:
+                return "freebsd-32";
+            case KnownPlatform::freebsd_64:
+                return "freebsd-64";
             case KnownPlatform::zos_z:
                 return "zos-z";
             default:
