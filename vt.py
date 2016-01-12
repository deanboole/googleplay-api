import sys
import virustotal

v = virustotal.VirusTotal("a264d77db499762fa7de5cf0372c2129a288ff38e02a81e8a4a736ec3667f214")
# report = v.get("downloaded_apks/2016-01-06_TOOLS_2_com.cleanmaster.mguard.apk")
report = v.scan(sys.argv[1])

print "Report"
print "- Resource's UID:", report.id
print "- Scan's UID:", report.scan_id
print "- Permalink:", report.permalink
print "- Resource's SHA1:", report.sha1
print "- Resource's SHA256:", report.sha256
print "- Resource's MD5:", report.md5
print "- Resource's status:", report.status
print "- Antivirus' total:", report.total
print "- Antivirus's positives:", report.positives
for antivirus, malware in report:
    if malware is not None:
        print
        print "Antivirus:", antivirus[0]
        print "Antivirus' version:", antivirus[1]
        print "Antivirus' update:", antivirus[2]
        print "Malware:", malware
