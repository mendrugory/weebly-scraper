#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import os
import datetime
import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen


MAX_FILE_NAME = 120
DATE_FORMAT = 'en'  # Put 'fr' here if your dates fit the format '%d/%m/%Y'


class WeeblyScraper():

    def scrape(self, weebly, target_folder):
        post_urls = []
        page_number = 1

        while True:
            address = weebly + '/blog/previous/' + str(page_number)
            print("Scraping page (" + address + ')')

            try:
                url = urlopen(address)
                soup = BeautifulSoup(url.read(), 'html.parser')

                if soup.find(id='blogTable') is not None:
                    for post in soup.findAll('a', {'class': 'blog-title-link'}):
                        formatted_url = "http:{}".format(post.get('href'))
                        post_urls.append(formatted_url)

                page_number += 1

            except:
                break

        print(post_urls)

        for post_url in post_urls:
            print(post_url)
            url = urlopen(post_url)
            soup = BeautifulSoup(url.read(), 'html.parser')

            title = soup.findAll('a', {'class': 'blog-title-link'})
            title = title[0].get_text().encode('utf-8', 'ignore')

            date = soup.findAll('p', {'class': 'blog-date'})
            date = date[0].get_text().encode('utf-8', 'ignore').strip()
            date = datetime.datetime.strptime(date.decode('utf-8'), '%d/%m/%Y').strftime('%Y-%m-%d')

            content = soup.findAll('div', {'class': 'blog-content'})
            content = content[0].prettify().encode('utf-8', 'ignore')

            url = post_url.replace(weebly, '').encode('utf-8', 'ignore')
            filename = url.decode('utf-8').replace('articles/', '')[:MAX_FILE_NAME]
            file_name = (target_folder + date + '-' + filename + '.md').replace("-/blog/", "-blog__")
            print("... writing " + date + '-' + filename + '.md')
            post_md = open(file_name, 'w+')
            post_md.write('---\ntitle: ' + '\"' + title.decode('utf-8').replace('\"', '\\\"') + '\"' + '\ndate: ' + date + "\nurl: " + url.decode('utf-8') + '\n---\n\n' + content.decode('utf-8').replace('  <', ' <'))
            get_images(soup, target_folder, file_name, weebly)
            post_md.close()


def get_images(soup, root_folder, post_file_name, weebly):
    folder_name = "{}/{}".format(root_folder, post_file_name.split("blog__")[1].split(".")[0])
    os.makedirs(folder_name)
    images = []
    for img in soup.findAll('img'):
        src = img.get('src')
        url_img = "http:{}".format(src) if src.startswith("//") else "{}{}".format(weebly, src) if src.startswith("/") else src
        filename = url_img.split('/')[-1]
        print("writing image {} ...".format(url_img))
        urllib.request.urlretrieve(url_img, "{}/{}".format(folder_name, filename))


if __name__ == '__main__':
    os.system("clear")
    print("Scrapping {}\n".format(sys.argv[1]))
    if len(sys.argv) != 3:
        print("\nUsage: `" + sys.argv[0] + " <Weebly URL posts\' page>   <Target Folder\' page>`\n")

    else:
        WeeblyScraper().scrape(sys.argv[1], sys.argv[2])

    sys.exit(0)
