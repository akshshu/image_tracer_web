import requests
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import re
import threading
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Required URL")
    parser.add_argument("-l", "--level", dest="level",
                        help="No of levels u wanna loook")
    options = parser.parse_args()
    if not options.level:
        options.level = 0
    if options.url[:4] != "http":
        parser.error("Please enter valid url, dont forget to add http https")
    checking_level = len(options.url.split("/"))
    return options.url, int(options.level)+checking_level


def request_check(url):
    try:
        status = requests.get(url).status_code
        if(status >= 200 and status < 400):
            return requests.get(url)
        else:
            pass
    except Exception:
        pass


def downlaod_image(img_url):
    img_bytes = requests.get(img_url)
    if(img_bytes.status_code >= 200 and img_bytes.status_code < 400):
        img_bytes = img_bytes.content
        img_name = img_url.split('/')[-1]
        try:
            with open(img_name, 'wb') as img_file:
                img_file.write(img_bytes)
                print(f"{img_name} downloaded")
        except Exception:
            pass
    else:
        pass


url, level = get_arguments()
global_list = []
global_list.append(url)
image_list = []
threads = []
url_parts = url.split("/")[2:]
compact_url = ''
for url_part in url_parts:
    compact_url += url_part


i = 0
while(i < len(global_list)):
    print("tuning into ", global_list[i])
    response = request_check(global_list[i])
    if response:
        link_list = re.findall('(?:href=")(.*?)"', str(response.content))
        for link in list(set(link_list)):
            link = urllib.parse.urljoin(url, link)
            if link not in global_list and len(link.split("/")) <= level:
                if (compact_url in link):
                    if(".css" not in link):
                        if(".pdf"not in link):
                            if(".js" not in link):
                                if(".zip"not in link):
                                    global_list.append(link)
                                    print(f'new link found {link}')
    else:
        pass

    i += 1
for link in global_list:
    response = request_check(link)
    if response:
        parsed_html = BeautifulSoup(response.content, features="html.parser")
        img_list = parsed_html.findAll("img")
        img_list = list(set(img_list))
        for image in img_list:
            img_src = image.get("src")
            img_src = urllib.parse.urljoin(url, img_src)
            image_list.append(img_src)
    else:
        pass
for img_url in list(set(image_list)):
    downlaod_image(img_url)
print(f'Download Completed')
