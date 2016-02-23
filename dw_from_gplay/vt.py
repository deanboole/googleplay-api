#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import logging
import virustotal
from db.Mongo import DB

logging.basicConfig(format='%(asctime)s %(message)s',
                    dtefmt='%Y-%m-%d %I:%M:%S',
                    level=logging.DEBUG)


class vt:

    def __init__(self):

        api_key = 'a264d77db499762fa7de5cf0372c2129a288ff38e02a81e8a4a736ec3667f214'
        self.v = virustotal.VirusTotal(api_key)

    def get(self, md5):
        """Return a anti-virus result, in dictionary type.
        """
        av_result = {}

        try:
            result = self.v.get(md5)

        except virustotal.VirusTotal.ApiError:
            logging.error("Maybe exceed the number of queries.")
            raise

        if result is None:
            return None

        av_result['summary'] = {}
        av_result['summary']['total'] = result.total
        av_result['summary']['positives'] = result.positives

        for antivirus, malware in result:
            av_result[antivirus[0]] = {}
            av_result[antivirus[0]]['version'] = antivirus[1]
            av_result[antivirus[0]]['result'] = malware

        return av_result

    def submit_sample(self, filename):
        """Submit APK which not in VT yet.
        """
        av_result = {}

        try:
            result = self.v.scan(filename)
            # self.v.scan(filename)

        except virustotal.VirusTotal.EntityTooLarge:
            logging.error("Exceed the limit of file size.")
            return None

        except virustotal.VirusTotal.ApiError:
            logging.error("Maybe exceed the number of queries.")
            raise

        result.join()
        av_result['summary'] = {}
        av_result['summary']['total'] = result.total
        av_result['summary']['positives'] = result.positives

        for antivirus, malware in result:
            av_result[antivirus[0]] = {}
            av_result[antivirus[0]]['version'] = antivirus[1]
            av_result[antivirus[0]]['result'] = malware

        return av_result


def main():

    try:
        db = DB()
    except:
        logging.error("DB error")
        raise

    while(True):
        doc = db.get_apk({'vt_scan': False, 'limit': 1})

        if not doc:
            logging.info("Maybe there's no document without vt_scan:true.")
            break

        av_result = vt().get(doc['md5'])

        if av_result is None:
            time.sleep(20)
            filename = '/tmp/'+doc['pgname']+'.apk'
            with open(filename, 'wb') as f:
                f.write(db.get_apk_file(doc['apkdata']))

            av_result = vt().submit_sample(filename)
            os.remove(filename)

            logging.info("Get av_result again")
            # It will try to get report with several queries,
            # so we take some sleep here.
            time.sleep(60)

        logging.debug("av_result: {}".format(av_result))
        db.update_av_report(doc['_id'], av_result)

        time.sleep(20)

if __name__ == "__main__":
    main()
