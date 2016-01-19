#!/bin/bash

t_stamp=`date +"%Y-%m-%d"`
categories=(APP_WIDGETS TOOLS WEATHER LIFESTYLE PRODUCTIVITY TRANSPORTATION SOCIAL MUSIC_AND_AUDIO PERSONALIZATION ENTERTAINMENT TRAVEL_AND_LOCAL FINANCE HEALTH_AND_FITNESS APP_WALLPAPER BUSINESS EDUCATION COMMUNICATION MEDIA_AND_VIDEO LIBRARIES_AND_DEMO NEWS_AND_MAGAZINES GAME SPORTS BOOKS_AND_REFERENCE COMICS SHOPPING MEDICAL PHOTOGRAPHY ANDROID_WEAR)


for category in ${categories[@]}; do

    # grap lists
    if [ ! -d "../download/applist_todownload/$t_stamp" ]; then
        mkdir -p ../download/applist_todownload/$t_stamp
    fi

    python list.py $category apps_topselling_free 1|cut -d';' -f 2 |grep -v "Package name" >> ../download/applist_todownload/$t_stamp/"$t_stamp"_"$category".txt

    # grep details
    if [ ! -d "../download/applist_todownload/$t_stamp" ]; then
        mkdir -p ../download/apk_detail_info/$t_stamp
    fi

    python list.py $category apps_topselling_free 1 > ../download/apk_detail_info/$t_stamp/"$t_stamp"_"$category"_detail.csv

    # download apks from lists
    n=1
    while read -r apk
    do
        python download.py "$apk"
        if [ ! -d "../download/downloaded_apks/$t_stamp" ]; then
            mkdir -p ../download/downloaded_apks/$t_stamp
        fi

        mv "$apk".apk ../download/downloaded_apks/$t_stamp/"$t_stamp"_"$category"_"$n"_"$apk".apk

        n=$(($n+1))
    done < ../download/applist_todownload/$t_stamp/"$t_stamp"_"$category".txt
done
