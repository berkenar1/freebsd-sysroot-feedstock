--- libmamba/src/specs/platform.cpp.orig	2026-05-05 00:00:00 UTC
+++ libmamba/src/specs/platform.cpp
@@ -128,6 +128,14 @@ namespace mamba::specs
 #elif defined(_WIN32)
         return KnownPlatform::win_32;
 
+#elif defined(__FreeBSD__)
+#if __x86_64__
+        return KnownPlatform::freebsd_64;
+#elif defined(i386)
+        return KnownPlatform::freebsd_32;
+#else
+#error "Unknown FreeBSD platform"
+#endif
 #else
 #error "Unknown platform"
 #endif
