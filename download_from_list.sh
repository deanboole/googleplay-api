#!/bin/bash

categories=(APP_WIDGETS TOOLS WEATHER LIFESTYLE PRODUCTIVITY TRANSPORTATION SOCIAL MUSIC_AND_AUDIO PERSONALIZATION ENTERTAINMENT TRAVEL_AND_LOCAL FINANCE HEALTH_AND_FITNESS APP_WALLPAPER BUSINESS EDUCATION COMMUNICATION MEDIA_AND_VIDEO LIBRARIES_AND_DEMO NEWS_AND_MAGAZINES GAME SPORTS BOOKS_AND_REFERENCE COMICS SHOPPING MEDICAL PHOTOGRAPHY ANDROID_WEAR)

# echo "" > download_lists.txt
#
# for category in ${categories[@]}; do
#     python list.py $category apps_topselling_free 10|cut -d';' -f 2 |grep -v "Package name" >> download_lists.txt
# done

while read -r apk
do
    python download.py "$apk"
    mv "$apk".apk downloaded_apks
done < download_lists.txt
