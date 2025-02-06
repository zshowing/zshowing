#coding=utf-8
import requests
from bs4 import BeautifulSoup
import time
import json
import os
import undetected_chromedriver as uc

# Constants
BASE_URL = "https://javdb.com"
ACTOR_URL = "/users/collection_actors"
COOKIE_PATH = "javdb.cookie"
WORKS_FILE = "javdb-works.json"
PROMPT_FILE = "javdb-prompt.txt"
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"

# Initialize saved works
saved_works = set()  # Use set for O(1) membership checks
prompt = ""

# Load previously saved works
if os.path.isfile(WORKS_FILE):
    with open(WORKS_FILE, "r") as f:
        saved_works = set(json.load(f))

# Parse cookies
def parse_cookies(cookie_string):
    return [{'name': name, 'value': value} for cookie in cookie_string.split('; ') for name, value in [cookie.split('=')]]

# Setup Chrome options
def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-application-cache')
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = uc.Chrome(options=options, version_main=132, use_subprocess=True, executable_path=CHROMEDRIVER_PATH)
    return driver

# Load cookies into driver
def load_cookies(driver, cookie_file):
    with open(cookie_file, "r") as f:
        cookie_string = f.read().replace("\n","")
    cookies = parse_cookies(cookie_string)
    driver.get(BASE_URL)
    driver.delete_all_cookies()
    time.sleep(3)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()

# Extract movie details from the movie page
def check_movie_for_magnets(driver, movieurl, fanhao):
    driver.get(f"{BASE_URL}{movieurl}")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    magnets_content = soup.find('div', {'id': 'magnets-content'})
    if magnets_content:
        magnets = magnets_content.find_all('div', class_='item')
        if magnets:
            print(f"Found magnet for {fanhao}")
            return True  # Movie has a magnet
    return False  # No magnet found

# Process each actor's collection
def process_actor(driver, actor):
    print(actor)
    nextpage = actor.find('a')
    detailUrl = nextpage.get('href')
    driver.get(f"{BASE_URL}{detailUrl}")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    movielist = soup.find('div', class_="movie-list")
    if movielist:
        movies = movielist.find_all('div', class_="item")
        for movie in movies:
            fanhaodiv = movie.find('div', class_='video-title')
            fanhao = fanhaodiv.find('strong').text
            title = fanhaodiv.text.strip()
            movieurl = movie.find('a').get('href')

            # Check if movie has a magnet
            if check_movie_for_magnets(driver, movieurl, fanhao):
                if fanhao in saved_works:
                    print(f"已移除 {title}")
                    saved_works.remove(fanhao)
                    prompt += f"{fanhaodiv.text}已出种！地址： https://javdb.com{movieurl}；"
                    print(f"{fanhaodiv.text} 出种子啦！")
                break
            else:
                if fanhao not in saved_works:
                    print(f"已记录 {title}")
                    saved_works.add(fanhao)
    time.sleep(3)

def main():
    # Setup driver and load cookies
    driver = setup_driver()
    load_cookies(driver, COOKIE_PATH)
    
    # Navigate to the actor collection page
    driver.get(f"{BASE_URL}{ACTOR_URL}")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    actors = soup.find_all('div', class_="actor-box")

    for actor in actors:
        process_actor(driver, actor)

    # Save the updated works list
    with open(WORKS_FILE, "w+") as f:
        json.dump(list(saved_works), f)

    # Handle prompt
    if prompt:
        with open(PROMPT_FILE, "w+") as f:
            f.write(prompt)
    else:
        if os.path.isfile(PROMPT_FILE):
            os.remove(PROMPT_FILE)
    
    driver.quit()

if __name__ == "__main__":
    main()
