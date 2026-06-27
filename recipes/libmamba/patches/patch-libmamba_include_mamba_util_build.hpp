--- libmamba/include/mamba/util/build.hpp.orig	2024-12-11 11:32:41 UTC
+++ libmamba/include/mamba/util/build.hpp
@@ -11,14 +11,22 @@ namespace mamba::util
 #if __APPLE__ || __MACH__
     inline static constexpr bool on_win = false;
     inline static constexpr bool on_linux = false;
     inline static constexpr bool on_mac = true;
+    inline static constexpr bool on_freebsd = false;
 #elif __linux__
     inline static constexpr bool on_win = false;
     inline static constexpr bool on_linux = true;
     inline static constexpr bool on_mac = false;
+    inline static constexpr bool on_freebsd = false;
+#elif __FreeBSD__
+    inline static constexpr bool on_win = false;
+    inline static constexpr bool on_linux = false;
+    inline static constexpr bool on_mac = false;
+    inline static constexpr bool on_freebsd = true;
 #elif _WIN32
     inline static constexpr bool on_win = true;
     inline static constexpr bool on_linux = false;
     inline static constexpr bool on_mac = false;
+    inline static constexpr bool on_freebsd = false;
 #else
 #error "no supported OS detected"
