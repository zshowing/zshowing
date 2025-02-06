#coding=utf-8
import requests
from bs4 import BeautifulSoup
import time
import json
import os
import undetected_chromedriver as uc

saved_works = []
prompt = ""

if os.path.isfile('javdb-works.json'):
	with open("javdb-works.json", "r") as f:
		saved_works = json.load(f)

def parse_cookies(cookie_string):
	cookies = []
	for cookie in cookie_string.split('; '):
		cookie = cookie.replace("\n", "")
		name, value = cookie.split('=')
		cookies.append({'name': name, 'value': value})
	return cookies

options = uc.ChromeOptions()
options.add_argument("--headless") # 设置为无头模式，即不显示浏览器窗口
options.add_argument("--disable-extensions") # 禁用扩展程序
options.add_argument("--disable-gpu") # 禁用GPU加速
options.add_argument("--no-sandbox") # 以沙盒模式运行
options.add_argument('--disable-application-cache')
options.add_argument("--disable-setuid-sandbox")
options.add_argument("--disable-dev-shm-usage")

cookie = ""
with open("javdb.cookie", "r") as f:
		cookie = f.read()

driver = uc.Chrome(options=options, version_main=132, use_subprocess=True, executable_path="/usr/local/bin/chromedriver")
url = "https://javdb.com"
driver.get(url)
driver.delete_all_cookies()
cookies = parse_cookies(cookie)
for cookie in cookies:
	driver.add_cookie(cookie)
url = "https://javdb.com/users/collection_actors"
driver.get(url)
html = driver.page_source
# response = requests.request("GET", url, headers=headers, data=payload, proxies=proxies)
# text = response.text
# text = req.content
# print(text)
text = html
soup = BeautifulSoup(text, features = 'html.parser')
actors = soup.find_all('div', class_="actor-box")
for actor in actors:
	nextpage = actor.find('a')
	detailUrl = nextpage.get('href')
	# response2 = requests.request("GET", "https://javdb.com" + detailUrl, headers=headers, data=payload, proxies=proxies)
	driver.get("https://javdb.com" + detailUrl)
	# text2 = response2.text
	text2 = driver.page_source
	soup2 = BeautifulSoup(text2, features = 'html.parser')
	movielist = soup2.find('div', class_="movie-list")
	movies = movielist.find_all('div', class_="item")
	for movie in movies:
		moviepage = movie.find('a')
		movieurl = moviepage.get('href')
		fanhaodiv = movie.find('div', class_='video-title')
		fanhao = fanhaodiv.find('strong').text
		title = fanhaodiv.text

		# response3 = requests.request("GET", "https://javdb.com" + movieurl, headers=headers, data=payload, allow_redirects=False, proxies=proxies)
		driver.get("https://javdb.com" + movieurl)
		text3 = driver.page_source
		# if response3.status_code == 302:
			# continue
		# text3 = response3.text
		soup3 = BeautifulSoup(text3, features = 'html.parser')
		magnets_content = soup3.find('div', {'id': 'magnets-content'})
		if magnets_content == None:
			continue
		magnets = magnets_content.find_all('div', class_='item')
		if len(magnets) == 0:
			if not any(saved_work == fanhao for saved_work in saved_works):
				print("已记录", title)
				saved_works.append(fanhao)
		else:
			if any(saved_work == fanhao for saved_work in saved_works):
				print("已移除", title)
				saved_works.remove(fanhao)
				prompt += fanhaodiv.text + "已出种！" + "地址： https://javdb.com" + movieurl + " ；"
				print(fanhaodiv.text, "出种子啦！")
			break
		print("Done check " + title)
		time.sleep(3)

with open("javdb-works.json", "w+") as f:
	json.dump(saved_works, f)

if prompt == "":
	if os.path.isfile('javdb-prompt.txt'):
		os.remove('javdb-prompt.txt')
else:
	with open("javdb-prompt.txt", "w+") as f:
		f.write(prompt)
