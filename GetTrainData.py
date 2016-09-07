#coding: utf-8
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://gunosy.com/"
response = urllib.request.urlopen(url)
html = response.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

	#range(1,9)で全てのカテゴリーの記事本文を取得する
for i in range(1,9):
# for i in range(1,2):
	f = open('category'+str(i)+'.txt', 'w')
	categories_link = soup.find(class_='nav_color_'+str(i)).find('a')
	print(categories_link.get('href'))
	categories_url = str(categories_link.get('href'))	
	print(categories_url)
	response = urllib.request.urlopen(categories_url)
	html = response.read().decode("utf-8")
	soup = BeautifulSoup(html, "html.parser")
	#range(2,52)で一つのカテゴリーから51*記事タイトル文だけ記事本文を取得する
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
		


		









