#!/usr/bin/python

# Do not remove
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

import sys
import argparse
from pprint import pprint

from config import *
from googleplay import GooglePlayAPI
from helpers import sizeof_fmt, print_header_line, print_result_line

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
    print "there's offset"
    offset = args.offset[0]
else:
    offset = None

api = GooglePlayAPI(ANDROID_ID)
api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
try:
    message = api.list(cat, ctr, nb_results, offset)
except:
    print "Error: HTTP 500 - one of the provided parameters is invalid"
    raise

if ctr is None:
    print SEPARATOR.join(["Subcategory ID", "Name"])
    for doc in message.doc:
        print SEPARATOR.join([doc.docid.encode('utf8'), doc.title.encode('utf8')])
else:
    print_header_line()
    doc = message.doc[0]
    for c in doc.child:
        print_result_line(c)
