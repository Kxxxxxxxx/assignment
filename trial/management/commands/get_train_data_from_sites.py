# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from getmostfrequentwords import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        import urllib.request
        from bs4 import BeautifulSoup
        from urllib.parse import urljoin
        import MeCab
        import collections

        # 以下でグノシーから教師データに用いる記事を取得
        url = "https://gunosy.com/"
        response = urllib.request.urlopen(url)
        html = response.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        for i in range(1,9):
        # for i in range(1,2):
        	f = open('trial/testwords/article_category'+str(i)+'.txt', 'w')
        	categories_link = soup.find(class_='nav_color_'+str(i)).find('a')
        	categories_url = str(categories_link.get('href'))	
        	print(categories_url)
        	response = urllib.request.urlopen(categories_url)
        	html = response.read().decode("utf-8")
        	soup = BeautifulSoup(html, "html.parser")
        	for j in range(2,52):
        	# for j in range(2,3):	
        		article_links = soup.find(class_='main').find_all(class_='list_title')
        		article_list_page = str(soup.find(class_='pager-link-option').find('a').get('href'))
        		for article_link in article_links:
        			article_url =str(article_link.find('a').attrs['href'])
        			response = urllib.request.urlopen(article_url)
        			html = response.read().decode("utf-8")
        			soup = BeautifulSoup(html, "html.parser")
        			article_contents = soup.find(class_='article gtm-click').find_all('p')
        			print(article_url)
        			for article in article_contents:
        				article_content = article.get_text()
        				f.write(article_content)
        			#記事内容を取得し終わったら次の記事リストページへ
        		response = urllib.request.urlopen(categories_url+'?page='+str(j))
        		html = response.read().decode("utf-8")
        		soup = BeautifulSoup(html, "html.parser")
        	f.close()

        #以下で教師データを生成
        # for i in range(1,2):
        for i in range(1,9):
        	f = open("trial/testwords/testwords_category"+str(i)+".txt","w")
        	trainwords = getmostfrequentwords('trial/testwords/article_category'+str(i)+'.txt')
        	for trainword in trainwords:
        		f.write(str(trainword[0]) + "\n")
        	f.close()



