import requests
import openai
import time
import os
from urllib.parse import quote,unquote,urlencode

headers = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'bid=7zyg7vIr5Go; ll="108288"; __utmc=30149280; push_doumail_num=0; __utmv=30149280.141; douban-fav-remind=1; ct=y; frodotk_db="cbd21e88d2f04c5563765b9a78d0e4ff"; gr_user_id=6c78f367-848e-45ac-9030-2a4b54e4cb0f; push_noty_num=0; apiKey=; dbcl2="1413857:Z4R5+FleFQE"; ck=9iCl; __utmz=30149280.1678620527.81.9.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1678629657%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_id.100001.8cb4=a365a81f964a2eec.1677587025.85.1678629657.1678621265.; _pk_ses.100001.8cb4=*; ap_v=0,6.0; __utma=30149280.1533361119.1677587027.1678620527.1678629660.82; __utmt=1; __utmb=30149280.2.10.1678629660; bid=vi1-QrygRos',
  'Origin': 'https://www.douban.com',
  'Referer': 'https://www.douban.com/people/zshowing/statuses',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"'
}

openai.api_key = os.environ.get('SCKEY')
url= 'https://m.douban.com/rexxar/api/v2/status/user_timeline/1413857?max_id=&ck=9iCl&for_mobile=1'

response = requests.request("GET", url, headers=headers)
result = response.json()
items = result['items']

isFirstStatus = True
latestId = ""
previousId = ""

if os.path.exists('status_id.txt'):
	with open('status_id.txt', 'r') as f:
		previousId = f.read().strip()

for item in items:
	itemtype = item['type']
	comments = item['comments']
	if itemtype == 'status':
		status = item['status']
		act = status['activity']
		text = status['text']
		statudid = status['id']
		if statudid == previousId:
			break
		if act == '说':
			if isFirstStatus:
				latestId = statudid
				isFirstStatus = False
			completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "从现在起，你将扮演一个在网络上回帖的用户。请试着在社交网络上对下列动态生成回复，除了回复的文字之外不含任何其他东西（但请不要只限于对文字的同意和奉承，最后有自己的见解或者引申出另外的内容）：" + text}])
			answer = "来自ChatGPT的回复：" completion.choices[0].message.content
			payload='rv_comment='+ quote(answer)+'&resp_type=c_dict&ck=9iCl'
			res = requests.request('POST', 'https://www.douban.com/j/status/'+ statudid + '/add_comment', data=payload, headers = headers)
			time.sleep(3)

with open('status_id.txt', 'w+') as f:
	f.write(latestId)
