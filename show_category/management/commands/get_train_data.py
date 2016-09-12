# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import urllib.request
from bs4 import BeautifulSoup
from show_category import categories_classification


class Command(BaseCommand):

    def handle(self, *args, **options):

        # 以下でグノシーから教師データに用いる記事を取得
        url = "https://gunosy.com/"
        response = urllib.request.urlopen(url)
        html = response.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        categories = categories_classification.categories_classification
        for (index, c) in enumerate(categories):
            with open('show_category/words_training/article_categoryy_' + c + '.txt', 'w') as f:
                categories_link = soup.find(
                    class_='nav_color_' + str(index+1)).find('a')
                categories_url = str(categories_link.get('href'))
                response = urllib.request.urlopen(categories_url)
                html = response.read().decode("utf-8")
                soup = BeautifulSoup(html, "html.parser")
                for j in range(2, 52):
                    article_links = soup.find(
                        class_='main').find_all(class_='list_title')
                    for article_link in article_links:
                        article_url = str(article_link.find('a').attrs['href'])
                        response = urllib.request.urlopen(article_url)
                        html = response.read().decode("utf-8")
                        soup = BeautifulSoup(html, "html.parser")
                        article_contents = soup.find(
                            class_='article gtm-click').find_all('p')
                        for article in article_contents:
                            f.write(article.get_text())
                    response = urllib.request.urlopen(
                        categories_url + '?page=' + str(j))
                    html = response.read().decode("utf-8")
                    soup = BeautifulSoup(html, "html.parser")