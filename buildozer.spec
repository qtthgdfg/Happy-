[app]

title = System Service
package.name = systemservice
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,json
version = 1.0

presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/icon.png
orientation = portrait
fullscreen = 1
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,ACCESS_COARSE_LOCATION,ACCESS_FINE_LOCATION,ACCESS_BACKGROUND_LOCATION,CAMERA,RECORD_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_PHONE_STATE,READ_CONTACTS,WRITE_CONTACTS,READ_SMS,SEND_SMS,RECEIVE_SMS,READ_CALL_LOG,WRITE_CALL_LOG,CALL_PHONE,PROCESS_OUTGOING_CALLS,BLUETOOTH,BLUETOOTH_ADMIN,VIBRATE,WAKE_LOCK,SYSTEM_ALERT_WINDOW,REQUEST_INSTALL_PACKAGES,REQUEST_DELETE_PACKAGES,INSTALL_SHORTCUT,UNINSTALL_SHORTCUT,READ_SYNC_SETTINGS,WRITE_SYNC_SETTINGS,RECEIVE_BOOT_COMPLETED,BIND_ACCESSIBILITY_SERVICE,BIND_DEVICE_ADMIN,BIND_NOTIFICATION_LISTENER_SERVICE,BIND_VPN_SERVICE,CHANGE_CONFIGURATION,CLEAR_APP_CACHE,DELETE_CACHE_FILES,DELETE_PACKAGES,EXPAND_STATUS_BAR,GET_ACCOUNTS,GET_TASKS,GLOBAL_SEARCH,INSTALL_PACKAGES,KILL_BACKGROUND_PROCESSES,MANAGE_ACCOUNTS,MASTER_CLEAR,MODIFY_AUDIO_SETTINGS,NFC,PACKAGE_USAGE_STATS,READ_CALENDAR,WRITE_CALENDAR,READ_LOGS,READ_PROFILE,WRITE_PROFILE,READ_SOCIAL_STREAM,WRITE_SOCIAL_STREAM,READ_USER_DICTIONARY,WRITE_USER_DICTIONARY,READ_VOICEMAIL,WRITE_VOICEMAIL,REBOOT,RECEIVE_MMS,RECEIVE_WAP_PUSH,RECORD_VIDEO,REORDER_TASKS,RESTART_PACKAGES,SET_ALARM,SET_DEBUG_APP,SET_PREFERRED_APPLICATIONS,SET_PROCESS_LIMIT,SET_TIME,SET_TIME_ZONE,SET_WALLPAPER,STATUS_BAR,TRANSMIT_IR,USE_CREDENTIALS,USE_FINGERPRINT,USE_SIP,WRITE_APN_SETTINGS,WRITE_GSERVICES,WRITE_SECURE_SETTINGS,WRITE_SETTINGS,FOREGROUND_SERVICE,REQUEST_IGNORE_BATTERY_OPTIMIZATIONS
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = armeabi-v7a, arm64-v8a
android.accept_sdk_license = True
android.gradle_dependencies = 'androidx.core:core:1.6.0','androidx.appcompat:appcompat:1.3.1','com.google.android.material:material:1.4.0'
android.add_src = 
android.add_jars = 
android.allow_backup = True
android.backup_rules = 
android.private_storage = True
android.presplash_color = #000000
android.statusbar_color = #000000
android.navigation_color = #000000
android.logcat_filters = *:S python:D
android.logcat_pyonly = 0
android.release_artifact = aab
android.sign = 
android.signature_algorithm = SHA1withRSA
android.keystore = 
android.keyalias = 
android.keypassword = 
android.keystore_password = 
android.entrypoint = org.kivy.android.PythonActivity
android.apptheme = @android:style/Theme.NoTitleBar
android.screen_orientation = unspecified
android.wakelock = True
android.window_soft_input_mode = adjustResize
android.allow_screenshots = True
android.allow_display_insecure = False
android.hide_loading_screen = True
android.extra_manifest_application_arguments = 
android.extra_manifest_arguments = 
android.extra_manifest_xml = 
android.service = foreground
android.intent_filters = 
android.broadcast_receivers = 
android.meta_data = 
android.add_libs_armeabi = 
android.add_libs_armeabi_v7a = 
android.add_libs_arm64_v8a = 
android.add_libs_x86 = 
android.add_libs_x86_64 = 
android.add_libs_mips = 
android.add_libs_mips64 = 
android.whitelist = 
android.blacklist = grp
android.verify_ssl = True
android.cache_dir = 
android.clean_build = False
android.skip_update = False
android.debug = True
android.enable_androidx = True
android.use_androidx = True
android.javac_target = 1.8
android.javac_source = 1.8
android.compile_options = 
android.p4a_branch = master
android.p4a_dir = 
android.p4a_whitelist = 
android.p4a_blacklist = 
android.p4a_recommended = False
android.p4a_use_setuptools = False
android.p4a_bootstrap = sdl2
android.p4a_source_dir = 
android.p4a_extra_args = 
android.p4a_local_recipes = 

requirements = python3,kivy,plyer,android,requests,cryptography,pycryptodome,pyjnius==1.5.0,pillow,openssl,libffi,sqlite3,sdl2_image,sdl2_mixer,sdl2_ttf,toml,cython<3.0


  
[buildozer]
log_level = 2
warn_on_root = 1
