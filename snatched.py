#!/usr/bin/env python3

import csv
import re
import operator

error = {}
per_user = {}
log = "/home/rtt/python/syslog.log"
reg = r": (ERROR|INFO) ([\w ']*).*\(([\w.]*)\)"

with open(log) as log:
  for line in log:
    try:
      unit, text, username = re.findall(reg, line)[0]
    except:
      continue
    if unit == "ERROR":
      error[text] = error.get(text,0) + 1
    if username not in per_user: per_user[username] = {}
    per_user[username][unit] = per_user[username].get(unit, 0) + 1


with open('error_message.csv', 'w') as errors:
  writer = csv.writer(errors)
  writer.writerow(['Error','Count'])
  for row in sorted(error.items(), key = operator.itemgetter(1), reverse = True):
    writer.writerow(row)

with open('user_statistics.csv','w') as stat:
  writer = csv.writer(stat)
  writer.writerow(['Username', 'INFO', 'ERROR'])
  for user in sorted(per_user):
    writer.writerow((user, per_user[user].get('INFO',0), per_user[user].get('ERROR',0)))
