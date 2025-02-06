# coding=utf-8
import requests
from bs4 import BeautifulSoup
import time
import json
import os
from concurrent.futures import ThreadPoolExecutor

# 配置文件路径
CONFIG = {
    "cookie_file": "javdb.cookie",
    "works_file": "javdb-works.json",
    "prompt_file": "javdb-prompt.txt",
    "base_url": "https://javdb.com"
}

# 加载已保存的作品列表
def load_saved_works():
    if os.path.isfile(CONFIG["works_file"]):
        with open(CONFIG["works_file"], "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 解析 Cookie 字符串为字典
def parse_cookies(cookie_string):
    return {item.split('=')[0]: item.split('=')[1] for item in cookie_string.split('; ')}

# 获取页面内容
def fetch_page(url, session):
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"请求失败: {url}, 错误: {e}")
        return None

# 检查作品是否有磁力链接
def check_movie(movie_url, session, saved_works):
    text = fetch_page(movie_url, session)
    if not text:
        return None

    soup = BeautifulSoup(text, "html.parser")
    magnets_content = soup.find('div', {'id': 'magnets-content'})
    if not magnets_content:
        return None

    magnets = magnets_content.find_all('div', class_='item')
    if not magnets:
        return "no_magnets"
    return "has_magnets"

# 处理单个演员的作品
def process_actor(actor_url, session, saved_works):
    text = fetch_page(actor_url, session)
    if not text:
        return []

    soup = BeautifulSoup(text, "html.parser")
    movies = soup.find_all('div', class_='item')
    results = []

    for movie in movies:
        movie_url = CONFIG["base_url"] + movie.find('a')['href']
        fanhao = movie.find('div', class_='video-title').find('strong').text
        title = movie.find('div', class_='video-title').text.strip()

        status = check_movie(movie_url, session, saved_works)
        if status == "no_magnets" and fanhao not in saved_works:
            results.append(("added", fanhao, title))
        elif status == "has_magnets" and fanhao in saved_works:
            results.append(("removed", fanhao, title, movie_url))
        time.sleep(1)  # 避免请求过快

    return results

# 主函数
def main():
    saved_works = load_saved_works()
    prompt = ""

    # 初始化 Session
    session = requests.Session()
    with open(CONFIG["cookie_file"], "r", encoding="utf-8") as f:
        session.cookies.update(parse_cookies(f.read()))

    # 获取演员列表
    actors_url = CONFIG["base_url"] + "/users/collection_actors"
    text = fetch_page(actors_url, session)
    if not text:
        return

    soup = BeautifulSoup(text, "html.parser")
    actors = soup.find_all('div', class_='actor-box')

    # 多线程处理演员作品
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_actor, CONFIG["base_url"] + actor.find('a')['href'], session, saved_works) for actor in actors]
        for future in futures:
            results = future.result()
            for result in results:
                if result[0] == "added":
                    saved_works.append(result[1])
                    print(f"已记录: {result[2]}")
                elif result[0] == "removed":
                    saved_works.remove(result[1])
                    prompt += f"{result[2]} 已出种！地址: {result[3]}\n"
                    print(f"{result[2]} 出种子啦！")

    # 保存更新后的作品列表
    with open(CONFIG["works_file"], "w", encoding="utf-8") as f:
        json.dump(saved_works, f)

    # 生成提示文件
    if prompt:
        with open(CONFIG["prompt_file"], "w", encoding="utf-8") as f:
            f.write(prompt)
    elif os.path.isfile(CONFIG["prompt_file"]):
        os.remove(CONFIG["prompt_file"])

if __name__ == "__main__":
    main()
