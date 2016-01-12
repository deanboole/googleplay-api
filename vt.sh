#!/bin/bash

for apk in $(ls downloaded_apks); do
    python vt.py downloaded_apks/$apk > vt-reports/vt_"$apk".txt
    sleep 16
done
