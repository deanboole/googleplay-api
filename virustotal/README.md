# Use VirusTotal API to scan gplay apks

```bash
# Submit apks to virustotal. Reports are in the vt-reports folder.
$ bash vt.sh

# Grep positive apks from reports.
$ bash vt-reports/detect_positive.sh

# Count number of positives in each category
$ bash vt-reports/category_count.sh
```
