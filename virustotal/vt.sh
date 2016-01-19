#!/bin/bash

t_stamp=`date +"%Y-%m-%d"`

for apk in $(ls ../download/downloaded_apks/$t_stamp); do
    python vt.py ../download/downloaded_apks/$t_stamp/$apk > vt-reports/vt_"$apk".txt
    sleep 16
done
