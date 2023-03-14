import requests
from datetime import datetime
import re
import json
import os

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

if os.path.exists('last163status.json'):
	with open('last163status.json', 'r') as f:
		data = json.load(f)
		count = int(data['count'])
		previous = datetime.strptime(data['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
		print(count, previous)

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
  response = requests.post(submiturl + token, data="params="+param2, headers=HEADERS)
if response.json()["code"] == 200:
	data = {"count": int(msg), "timestamp": now}
	with open('last163status.json', 'w+') as f:
		json.dump(data, f, default=str)
		print("Done re-submitting.        ", end ='\r')
	with open('163-output.txt', 'w+') as f:
		f.write('Done re-submitting,' + ", time using: " + str(now - previous).split('.', 2)[0])
	return 0
elif int(msg) == 0:
	with open('last163status.json', 'w+') as f:
		data = {"count": 0, "timestamp": now}
		json.dump(data, f, default=str)
	with open('163-output.txt', 'w+') as f:
		f.write('Reset the count to 0')
	return 0
else:
	print("No feedback.", end='\r')
	return 1

