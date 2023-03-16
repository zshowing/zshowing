#coding=utf-8
import requests
from bs4 import BeautifulSoup
import time
import json
import os
import undetected_chromedriver as uc

url = "https://javdb.com/users/collection_actors"
saved_works = []
prompt = ""

if os.path.isfile('javdb-works.json'):
	with open("javdb-works.json", "r") as f:
		saved_works = json.load(f)

payload={}
proxies = {
    'http': 'http://localhost:9910',  # 设置HTTP代理
    'https': 'http://localhost:9910'  # 设置HTTPS代理
}
headers = {
  'authority': 'javdb.com',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6',
  'cache-control': 'max-age=0',
  'cookie': 'list_mode=h; theme=auto; locale=zh; over18=1; _ym_uid=1678595611806523704; _ym_d=1678595611; remember_me_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkltOVNPRlZaTWxrNVdFTktTRlpWVlRWWmNYUnFJZz09IiwiZXhwIjoiMjAyMy0wMy0xOVQwNDozNzozMy4wMDBaIiwicHVyIjoiY29va2llLnJlbWVtYmVyX21lX3Rva2VuIn19--4ef12d6cd87106ba46037155a6fa3b17f09d43ef; _ym_isad=1; _jdb_session=L8v7bXoXtWD0jlPCkjucQOptG5niRNlSUYRSWtc0IHeIpnfyjGe0Q7Pfv6kTCjj2p2gqqt0jn%2FOjSF87T7rELQa5%2FtGRQQjG5rxruUczT7pnsroIC1gVOTATeZRw1fc3QKKdN25KzFnSdGf2WcSMQzHJlqkeKpCJaZkQq3fRfdVg9L9j%2BKnZ5Q1%2BnQcvzwRDTSTTBbqQQM5bFYeNeIYJdWEPrVzPIuqrCxhByhBCFjrSoRRT7OGRJeA706OwjufUagNWgfZfG29GULkli8lJ%2FfJl4bMywij8h%2BM5qydTjZNqthN7xD9lXy%2Baw4j3hOZFKN%2FmfIVRORJs6parQlHnPh%2F9aQsA%2BYHJ0tjhaf4Q7900%2FSklJ46H1wLoaJ1QxQ%2FbfhA%3D--GNI0HSan1XZ9aVe8--TPBxqRNL1oN8zY8XipKs4w%3D%3D; _jdb_session=xpJJ8wWlI9X9bG4cCrhD6JCGuLZPoG44oqdmewju6W0QwVXkI8246Va5S3tmJfTNwDE%2Fmwb%2FUvl0BJZlpEJbkuOYfNcSMTE797WE46%2BzKGOBkSoV4tZ7OGZAqT%2BjnZDZPqtm9a%2B0bScp%2BxfslBgG2wkq2SooP2k8%2BgC%2BrYTemm2wA7AXF2VxyVONMuKHEZSRo5D1JemC4NT%2FVafCKwUjsiw2Z5hv0mgYgUPLAGNVfkEyQt%2Fyaehfde4ROy9bHY%2FnQkrBNrdwCiJlQpl5uvqFjRFa2uiOsrDp0iF5JI1yVGwBkH65vC1%2FNwnTkkhrw6knW7cZ8FFMcJ8dW0%2Bc%2BuqUhjX8k0QtT%2FKFYx0Hz6pQX6J9TFiLmx%2B8ssu8aqLx1%2BRhMVY%3D--3DKr2xHyLlNnXOfZ--rxBvN%2Bk0mXea%2Ft8g9s6IPQ%3D%3D; locale=zh',
  'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

options = uc.ChromeOptions()
options.add_argument("--headless") # 设置为无头模式，即不显示浏览器窗口
options.add_argument("--disable-extensions") # 禁用扩展程序
options.add_argument("--disable-gpu") # 禁用GPU加速
options.add_argument("--no-sandbox") # 以沙盒模式运行
options.add_argument('--disable-application-cache')
options.add_argument("--disable-setuid-sandbox")
options.add_argument("--disable-dev-shm-usage")

# 设置请求头
options.add_argument("user-agent=" + headers['user-agent'])
options.add_argument("cookie=" + headers['cookie'])

with uc.Chrome(options=options, version_main = 110) as driver:
	for cookie in cookies:
		driver.add_cookie(cookie)
		driver.get(url)
		time.sleep(3)
		html = driver.page_source
		print(html)
# response = requests.request("GET", url, headers=headers, data=payload, proxies=proxies)
# text = response.text
# text = req.content
# print(text)
text = ""
soup = BeautifulSoup(text, features = 'html.parser')
actors = soup.find_all('div', class_="actor-box")
for actor in actors:
	nextpage = actor.find('a')
	detailUrl = nextpage.get('href')
	response2 = requests.request("GET", "https://javdb.com" + detailUrl, headers=headers, data=payload, proxies=proxies)
	text2 = response2.text
	soup2 = BeautifulSoup(text2, features = 'html.parser')

	movielist = soup2.find('div', class_="movie-list")
	movies = movielist.find_all('div', class_="item")
	
	for movie in movies:
		moviepage = movie.find('a')
		movieurl = moviepage.get('href')
		fanhaodiv = movie.find('div', class_='video-title')
		fanhao = fanhaodiv.find('strong').text
		title = fanhaodiv.text

		response3 = requests.request("GET", "https://javdb.com" + movieurl, headers=headers, data=payload, allow_redirects=False, proxies=proxies)
		if response3.status_code == 302:
			continue
		text3 = response3.text
		soup3 = BeautifulSoup(text3, features = 'html.parser')
		magnets_content = soup3.find('div', {'id': 'magnets-content'})
		magnets = magnets_content.find_all('div', class_='item')
		if len(magnets) == 0:
			if not any(saved_work == fanhao for saved_work in saved_works):
				print("已记录", title)
				saved_works.append(fanhao)
		else:
			if any(saved_work == fanhao for saved_work in saved_works):
				print("已移除", title)
				saved_works.remove(fanhao)
				prompt += fanhaodiv.text + "已出种！" + "地址： https://javdb.com" + movieurl + " \n"
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