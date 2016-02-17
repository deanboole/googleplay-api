#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        """Return a anti-virus result, in dictionary
        """
        av_result = {}

        try:
            result = self.v.get(md5)

        except:
            logging.error("Maybe exceed the number of queries.")
            return None

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

    doc = db.get_apk({'av_result': {'$exists': False}, 'limit': 1})

    av_result = vt().get(doc['md5'])

    if av_result is not None:
        db.update_av_report(doc['_id'], av_result)

if __name__ == "__main__":
    main()
