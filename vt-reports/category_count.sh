#!/bin/bash

categories=(APP_WIDGETS TOOLS WEATHER LIFESTYLE PRODUCTIVITY TRANSPORTATION SOCIAL MUSIC_AND_AUDIO PERSONALIZATION ENTERTAINMENT TRAVEL_AND_LOCAL FINANCE HEALTH_AND_FITNESS APP_WALLPAPER BUSINESS EDUCATION COMMUNICATION MEDIA_AND_VIDEO LIBRARIES_AND_DEMO NEWS_AND_MAGAZINES GAME SPORTS BOOKS_AND_REFERENCE COMICS SHOPPING MEDICAL PHOTOGRAPHY ANDROID_WEAR)

 for category in ${categories[@]}; do

     num=$(grep positive *|grep -v "Antivirus's positives: 0"|grep "$category" |wc -l)
     echo "$category; $num"
     #grep positive *|grep -v "Antivirus's positives: 0"|grep "$category" |wc -l
 done
