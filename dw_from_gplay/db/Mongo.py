#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import gridfs
from pymongo import MongoClient

from ConfigParser import ConfigParser


class DB():

    def __init__(self, config_name='TEST'):

        # Read db.config
        config_file = os.path.dirname(__file__)+"/db.conf"
        parser = ConfigParser()
        parser.read(config_file)

        db_server = parser.get(config_name, 'ip')
        db_name = parser.get(config_name, 'database')

        try:
            conn = MongoClient(host=db_server)
        except:
            logging.error("DB connect error!")
        finally:
            logging.debug("Using DB server: {0}, DB: {1}".format(db_server,
                                                                 db_name))
            self.db = conn[db_name]
            self.fs = gridfs.GridFS(self.db)

        self.ensure_index()

    def ensure_index(self):
        self.db.fs.files.ensure_index(
            'filename', unique=True, background=True)

    def insert_apk(self, payload):
        """This function inserts the apk & information to mongo DB.

        Args:
            payload (dict): APK file & information.

        >>>insert_apk({binary:'foo', version:'0.1', name:'bar'})

        """

        expected_fields = ('source',
                           'submit_date', # date of APK submit to DB
                           'name',
                           'version',
                           'size',
                           'requirements',
                           'pgname',
                           'upload_date', # date of APK publish
                           'apkdata',
                           'title',
                           'sub_title',
                           'rank',
                           'sha1',
                           'crc32',
                           'ssdeep',
                           'sha256',
                           'sha512',
                           'md5'
                           )

        # filter unexpect fields
        for key in payload.keys():
            if key not in expected_fields:
                payload.pop(key)

        # insert file to gridfs and check if file is already existed
        if self.fs.exists(filename=payload['sha512']):
            logging.debug(
                "{0} File already exists!".format(
                    payload['filename']))
            file_id = self.db.fs.files.find_one(
                {'filename': payload['sha512']})['_id']
        else:
            file_id = self.fs.put(
                payload['apkdata'],
                filename=payload['sha512'])

        payload['apkdata'] = file_id

        # insert data to apk collection
        try:
            self.db.apk.insert_one(payload)
        except:
            logging.info("Error insert data!")
