#!/bin/bash

t_stamp=`date +"%Y-%m-%d"`

if [ ! -d "andro-reports" ]; then
  mkdir -p andro-reports/$t_stamp
fi

for apk in $(ls download/downloaded_apks/$t_stamp); do
    python androinfo.py download/downloaded_apks/$t_stamp/$apk > andro-reports/$t_stamp/ag_"$apk".txt
done
