#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import Blueprint, render_template, request, make_response

ui = Blueprint('ui', __name__)


@ui.route('/all_apks/', methods=['GET'])
def all_apks():
    from db.Mongo import DB

    # result = DB().get_apk({'title': 'APP_WIDGETS'})
    result = DB().get_apk({})

    return render_template('all_apks.html',
                           apks=result)


@ui.route('/', methods=['GET'])
@ui.route('/daily_apks/', methods=['GET'])
def daily_apks():
    import datetime
    from db.Mongo import DB

    today = datetime.datetime.strftime(
        datetime.datetime.today() -
        datetime.timedelta(days=1), '%Y-%m-%d')
    db_result = list(DB().get_apk({'submit_date': today}))

    categories_result = daily_apks_by_categories(db_result)
    antivirus_result = daily_apks_by_antivirus(db_result)

    return render_template('daily_apks.html',
                           date=today,
                           categories=categories_result,
                           antivirus=antivirus_result
                           )


def daily_apks_by_categories(db_result):

    result = {}

    for i in db_result:
        if i['title'] in result:
            result[i['title']][i['rank']] = i

        else:
            result[i['title']] = {}
            result[i['title']][i['rank']] = i

    # return render_template('daily_category.html',
    #                        date=today,
    #                        categories=result)

    return result


def daily_apks_by_antivirus(db_result):

    result = {}

    for i in db_result:
        if 'av_result' in i:
            if i['av_result']['summary']['positives'] > 0:
                if i['av_result']['summary']['positives'] in result:
                    result[i['av_result']['summary']['positives']]['name'] = i

                else:
                    result[i['av_result']['summary']['positives']] = {}
                    result[i['av_result']['summary']['positives']]['name'] = i

    # return render_template('daily_antivirus.html',
    #                        date=today,
    #                        times=result)

    return result


@ui.route('/all_apks/download/', methods=['POST'])
@ui.route('/daily_apks/download/', methods=['POST'])
def download_apk():
    """Get document Objectid and Download APK file
    """
    from db.Mongo import DB
    from bson.objectid import ObjectId

    my_db = DB()
    apk_id = request.form['download_apk']

    apk_info = my_db.get_apk({'_id': ObjectId(apk_id), 'limit': 1})
    logging.debug(
        'Download {}, {}'.format(apk_info['md5'], apk_info['apkdata']))
    apkdata = my_db.get_apk_file(apk_info['apkdata'])

    response = make_response(apkdata)
    response.headers['Content-Type'] = 'application/vnd.android.package-archive'
    response.headers['Content-Disposition'] = 'attachment; filename='+apk_info['pgname']+".apk"

    return response


@ui.route('/mytest/', methods=['GET'])
def mytest():

    return render_template('mine.html',)
