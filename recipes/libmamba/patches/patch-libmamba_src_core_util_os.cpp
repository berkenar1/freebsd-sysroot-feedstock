--- libmamba/src/core/util_os.cpp.orig	2026-05-05 00:00:00 UTC
+++ libmamba/src/core/util_os.cpp
@@ -12,6 +12,10 @@
 #if defined(__APPLE__)
 #include <libproc.h>
 #include <mach-o/dyld.h>
+#endif
+#if defined(__FreeBSD__)
+#include <sys/sysctl.h>
+#include <sys/user.h>
 #endif
 #include <inttypes.h>
 #include <limits.h>
@@ -351,6 +355,29 @@ namespace mamba
 
         return ret;
     }
+#elif defined(__FreeBSD__)
+    std::string get_process_name_by_pid(const int pid)
+    {
+        int mib[4];
+        struct kinfo_proc ki;
+        size_t len;
+
+        mib[0] = CTL_KERN;
+        mib[1] = KERN_PROC;
+        mib[2] = KERN_PROC_PID;
+        mib[3] = pid;
+
+        len = sizeof(ki);
+        if (sysctl(mib, 4, &ki, &len, NULL, 0) < 0)
+        {
+            return "";
+        }
+        if (len == 0)
+        {
+            return "";
+        }
+        return ki.ki_comm;
+    }
 #elif defined(__linux__)
     std::string get_process_name_by_pid(const int pid)
     {
