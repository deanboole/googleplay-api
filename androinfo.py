#!/usr/bin/env python

import sys
sys.path.append("/usr/share/androguard/")

from androguard.core.bytecodes import dvm, apk
from androguard.core.analysis import analysis
from androguard.decompiler.dad import decompile
#from androguard.core.analysis import ganalysis

pathtofile = "downloaded_apks/2016-01-06_TOOLS_10_tw.nitcs.tmpclear.apk"

# information about files, permissions and different entry points(activities, services...)
a = apk.APK(sys.argv[1])
print "PACKAGE NAME:", "["+a.get_package()+"]"
#a.show()
#print a.get_activities()
#print a.androidversion
print "TARGET SDK VERSION:", "["+a.get_target_sdk_version()+"]"
print "MIN SDK VERSION:", "["+a.get_min_sdk_version()+"]"
print "Permissions:", str(a.get_permissions())
