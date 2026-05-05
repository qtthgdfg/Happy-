# service.py - Android background service entry point
# This file is referenced in buildozer.spec under [app] services
# and provides the entry point for the Android background service

import sys
import os

# Add the app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """
    Entry point for Android PythonService.
    This is called when the service starts.
    """
    print("[Service] PythonService main() called")
    
    try:
        # Import the Android service wrapper from main module
        from main import AndroidServiceWrapper, ANDROID_SERVICE, ANDROID_AVAILABLE, WALLET_ADDRESS
        
        if not ANDROID_AVAILABLE:
            print("[Service] ERROR: Android not available")
            return
        
        if not ANDROID_SERVICE:
            print("[Service] ERROR: No service instance")
            return
        
        if WALLET_ADDRESS == "YOUR_WALLET_ADDRESS_HERE":
            print("[Service] ERROR: Wallet address not set")
            return
        
        print("[Service] Creating service wrapper...")
        wrapper = AndroidServiceWrapper(ANDROID_SERVICE)
        
        print("[Service] Starting service...")
        success = wrapper.on_start()
        
        if success:
            print("[Service] Service started successfully")
            # Keep service alive
            import time
            while wrapper.running:
                time.sleep(5)
            print("[Service] Service stopped")
        else:
            print("[Service] Failed to start service")
    
    except Exception as e:
        print(f"[Service] Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
