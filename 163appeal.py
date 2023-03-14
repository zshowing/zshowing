import requests
import time
from datetime import datetime
import sys
import re

token = ""
counturl = "https://music.163.com/weapi/pl/count"
historyurl = "https://music.163.com/weapi/msg/private/history"
submiturl = "https://music.163.com/weapi/gorilla/gateway/appeal/submit"
clearurl = "https://music.163.com/weapi/msg/count/clear"
param1 = ""
param2 = ""
cookie = ""
count = 0

previous = 0

f = open('163cookies.txt')
for line in f:
  result = re.search('csrf_token=([a-z0-9]+)', line)
  result2 = re.search('\'cookie: (.*)\'', line)
  result3 = re.search('\'params=(.*)\'', line)
  if result and len(token) == 0:
    token = "?csrf_token=" + result.group(1)
  elif result2:
    cookie = result2.group(1)
  elif result3:
    if len(param1) == 0:
      param1 = result3.group(1)
    elif len(param2) == 0:
      param2 = result3.group(1)
f.close()

HEADERS = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6',
    'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    'referer':'https://music.163.com/msg/',
    'content-type': 'application/x-www-form-urlencoded',
    'authority': 'music.163.com',
    'origin': 'https://music.163.com',
    'nm-gcore-status': '1',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "macOS",
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'cookie': cookie
}

if len(sys.argv) > 1:
  datestr = datetime.now().strftime('%b %d %Y')
  previous = datetime.strptime(datestr + " " + sys.argv[1], '%b %d %Y %H:%M')

print("Checking counts...        ", end='\r')
response = requests.post(counturl + token, 
  data="params="+param1, 
  headers=HEADERS)
msg = response.json()['msg']

if count == 0:
  count = int(msg) - 1

if int(msg) > count:
  print("Eureka!                ", end='\r')
  now = datetime.now()
  current_time = now.strftime("%H:%M")
  if isinstance(previous, datetime):
    print("Got a respond at " + current_time + ", time using: " + str(now - previous).split('.', 2)[0] )
  else:
    print("Got a respond at " + current_time + ".")
  previous = datetime.now()
  response = requests.post(submiturl + token, 
    data="params="+param2,
    headers=HEADERS)
  if response.json()["code"] == 200:
    count += 1
    print("Done re-submitting.        ", end ='\r')
else:
  now = datetime.now()
  current_time = now.strftime("%H:%M")
  print("No feedback at " + current_time + ".", end='\r')

