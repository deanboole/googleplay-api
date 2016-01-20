# Google Play APKs Analysis

### Setup

```bash
$ git clone https://github.com/deanboole/googleplay-api.git
$ virtualenv googleplay-api
$ cd googleplay-api
$ source bin/activate
$ pip install -r requirements.txt
```

### Module function
```bash
# Generate apk download lists, details and the most important of all, download apks.
$ bash dw_from_gplay/download_from_lists.sh

# Submit apks to virustotal. Reports are in the vt-reports folder.
$ bash virustotal/vt.sh

# Grep positive apks from reports.
$ bash virustotal/vt-reports/detect_positive.sh

# Count number of positives in each category
$ bash virustotal/vt-reports/category_count.sh

# Auto Static analysis via androguard
$ bash andro-analysis/androguard-report.sh

# Open Jadx GUI and start to analyze
$ ./bin/jadx-gui
```
