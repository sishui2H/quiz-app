[app]

# (str) Title of your application
title = 毛概答题练习系统

# (str) Package name
package.name = quizapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.quiz

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,docx

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,images/*,给学生的练习题*.docx

# (list) Source files to ignore (let empty to ignore nothing)
source.ignore_patterns = license,images/*/*.jpg,__pycache__/*

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,python-docx,lxml

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
# garden_requirements =

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
# services = NAME:ENTRYPOINT

#
# OSX Specific
#

#
# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 2.0.0

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
# android.presplash_color = #FFFFFF

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
# android.sdk = 20

# (str) Android NDK version to use
# android.ndk = 19b

# (int) Android NDK API to use. This is the minimum API your app will support.
# android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
# android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
# android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
# android.sdk_path =

# (str) ANT executable (if empty, it will be automatically downloaded.)
# android.ant_path =

# If you want to manually define where the Android SDK/NDK/... are
# you might prefer to set android.use_aapt2 to "auto"
# If you set to True, buildozer will use aapt2 instead of aapt
# If you set to False, buildozer will use aapt instead of aapt2
# android.use_aapt2 = auto

# (str) Android entry point, default is ok for Kivy based application.
# android.entrypoint = org.kivy.android.PythonActivity

# (list) Pattern to whitelist for the whole project
# android.whitelist =

# (list) Path to libraries to add to the project.
# android.add_libs =

# (list) Pattern to whitelist for the whole project
# android.whitelist =

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = arm64-v8a

#
# Python for android (p4a) specific
#

# (str) python-for-android fork to use, defaults to upstream (kivy)
# p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
# p4a.branch = master

# (str) python-for-android specific commit to use, defaults to HEAD, must be within p4a.branch
# p4a.commit = HEAD

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
# p4a.source_dir =

# (str) The directory in which python-for-android should look for your own build recipes (if any)
# p4a.local_recipes =

# (str) Filename to the hook for p4a
# p4a.hook =

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit port for the local server
# p4a.local_server_port = 8080

# (list) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit port for the local server
# p4a.local_server_port = 8080

#
# iOS specific
#

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
# ios.codesign.debug = "iPhone Developer: &lt;lastname&gt; &lt;firstname&gt; (&lt;hexid&gt;)"

# (str) Name of the certificate to use for signing the release version
# ios.codesign.release = %(ios.codesign.debug)s


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# buildozer.build_artifacts = bin

# (int) If true, save downloaded packages in buildozer global directory.
# buildozer.cache_dir = ~/.buildozer/cache

# (int) If true, don't build the python-for-android bootstrap
# buildozer.bootstrap_build = False
