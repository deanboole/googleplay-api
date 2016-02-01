#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import Blueprint, render_template, request, make_response

ui = Blueprint('ui', __name__)


@ui.route('/', methods=['GET'])
@ui.route('/daily_apks/', methods=['GET'])
def apk():
    from db.Mongo import DB

    # result = DB().get_apk({'title': 'APP_WIDGETS'})
    result = DB().get_apk({})

    return render_template('apk.html',
                           attacks=result)


@ui.route('/apk/download/', methods=['POST'])
def download_apk():
    from db.Mongo import DB

    my_db = DB()
    md5 = request.form['download_apk']
    apk_info = my_db.get_apk({'md5': md5, 'limit': 1})
    logging.debug('Download {}, {}'.format(apk_info['md5'], apk_info['apkdata']))
    apkdata = my_db.get_apk_file(apk_info['apkdata'])

    response = make_response(apkdata)
    response.headers['Content-Type'] = 'application/vnd.android.package-archive'
    response.headers['Content-Disposition'] = 'attachment; filename='+apk_info['pgname']+".apk"

    return response
