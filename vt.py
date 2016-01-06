import simplejson
import urllib
import urllib2

import sys

url = "https://www.virustotal.com/vtapi/v2/url/report"
parameters = {"resource": str(sys.argv[1]),
              "apikey": "fill in your key"}
data = urllib.urlencode(parameters)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
json = response.read()

print json
