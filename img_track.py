import threading
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import urllib.parse
import requests
import os
import argparse
import sys
thread_list = []


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("web", help="Mention website")
    parser.add_argument("dest", help="Mention location")
    options = parser.parse_args()
    return options.web, options.dest


def get_source(url):
    print("\rLoading Page Source...", end="")
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    return driver.page_source


def get_img_links(url, html):
    img_links = []
    soup = BeautifulSoup(html, features="html.parser")
    img_list = soup.findAll("img")
    img_list = list(set(img_list))
    for image in img_list:
        img_src = image.get("src")
        if(img_src == ""):
            img_src = image.get("data-src")
        if(img_src==None):
        	continue
        img_src = urllib.parse.urljoin(url, img_src)
        img_links.append(img_src)
    return img_links


def path_create(directory):
    current_dir = os.getcwd()
    path = os.path.join(current_dir, directory)
    os.mkdir(path)
    return path


def download_image(img_url, path):
    status = requests.get(img_url).status_code
    if(status == 200):
        try:
            img_bytes = requests.get(img_url).content
        except Exception:
            return
        img_name = img_url.split("/")[-1]
        if img_name != "":
            img_path = path+"/"+img_name
            try:
                with open(img_path, 'wb') as image:
                    image.write(img_bytes)
                    print(f"{img_name} downloaded")
                	
            except Exception:
                return
        else:
            pass

    else:
        pass


url, directory = get_arguments()
path = path_create(directory)
html = get_source(url)
sys.stdout.flush()
print("\rPage source loaded.")
img_links = get_img_links(url, html)
sys.stdout.flush()
print(f"\rTotal Images Found :{len(list(set(img_links)))}")
for image in list(set(img_links)):
    t=threading.Thread(target=download_image,args=[image, path])
    t.start()
    thread_list.append(t)
for thrd in thread_list:
	thrd.join()

