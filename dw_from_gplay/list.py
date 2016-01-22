#!/usr/bin/python

# Do not remove
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

from datetime import datetime, timedelta
import logging
import argparse
from pprint import pprint

from config import *
from db.Mongo import DB
from common.objects import File
from googleplay import GooglePlayAPI
from helpers import sizeof_fmt, print_header_line, print_result_line

logging.basicConfig(format='%(asctime)s %(message)s',
                                        dtefmt='%Y-%m-%d %I:%M:%S',
                                        level=logging.DEBUG)

parser = argparse.ArgumentParser(description='List subcategories and \
                                 apps within them.')

parser.add_argument("category", nargs=1, type=str,
                    help='To obtain a list of supported catagories, \
                    use categories.py')

parser.add_argument("subcategory", nargs=1, type=str, default=None,
                    help='You can get a list of all subcategories available, \
                    by supplying a valid category')

parser.add_argument("nb_results", nargs=1, type=str, default=None,
                    help='You can get a list of all subcategories available, \
                    by supplying a valid category')

parser.add_argument("--offset", nargs=1, type=int, default=None,
                    help='You can get a list of all subcategories available, \
                    by supplying a valid category')

args = parser.parse_args()
cat = args.category[0]
ctr = args.subcategory[0]
nb_results = args.nb_results[0]
if args.offset:
    logging.debug("there's offset : {}".format(args.offset))
    offset = args.offset[0]
else:
    offset = None

api = GooglePlayAPI(ANDROID_ID)
api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
try:
    message = api.list(cat, ctr, nb_results, offset)
except:
    logging.error("Error: HTTP 500 - one of the provided parameters is invalid")
    raise

today = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
rank = 1
for i in message.doc[0].child:

    result = {}

    # submit_date
    result['submit_date'] = today

    # source
    result['source'] = 'googleplay'

    # category(title)
    result['title'] = cat
    # print cat
    # subcategory(title)
    result['sub_title'] = ctr
    # APK name
    result['name'] = unicode(i.title).encode('utf8')
    # print unicode(i.title).encode('utf8')
    # rank
    result['rank'] = rank
    # print rank
    # Packagename
    result['pgname'] = i.details.appDetails.packageName
    # print i.details.appDetails.packageName
    # APK version
    result['version'] = i.details.appDetails.versionCode
    # print i.details.appDetails.versionCode
    # APK size
    result['size'] = sizeof_fmt(i.details.appDetails.installationSize)
    # print sizeof_fmt(i.details.appDetails.installationSize)
    # Upload date
    result['upload_date'] = datetime.strptime(unicode(i.details.appDetails.uploadDate).encode('utf8'),
                                              "%Y\345\271\264%m\346\234\210%d\346\227\245").strftime('%Y-%m-%d')
    # print datetime.strptime(unicode(i.details.appDetails.uploadDate).encode('utf8'),
    #                         "%Y\345\271\264%m\346\234\210%d\346\227\245").strftime('%Y-%m-%d')

    # Download APK
    result['apkdata'] = api.download(i.details.appDetails.packageName,
                                     i.details.appDetails.versionCode,
                                     i.offer[0].offerType)
    result.update(File(result['apkdata']).result)

    rank += 1
    try:
        DB().insert_apk(result)
    except KeyError:
        logging.warn("Maybe the apk already exists: {}".format(result['pgname']))
        continue
    except:
        logging.error("DB insert error: {}".format(result['pgname']))
        raise
"""
if ctr is None:
    print SEPARATOR.join(["Subcategory ID", "Name"])
    for doc in message.doc:
        print doc
        # print SEPARATOR.join([doc.docid.encode('utf8'), doc.title.encode('utf8')])
else:
    # print_header_line()
    doc = message.doc[0]
    for c in doc.child:
        print_result_line(c)
"""

