# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from show_category import get_words_from_text
import urllib.request
from bs4 import BeautifulSoup
import pickle


class Command(BaseCommand):

    def handle(self, *args, **options):
        categories = ["entertainment", "sports", "fun", "domestic",
                      "abroad", "column", "it_science", "gourmet"]
        # 以下でグノシーから教師データに用いる記事を取得
        url = "https://gunosy.com/"
        response = urllib.request.urlopen(url)
        html = response.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        index = 0
        for c in categories:
            index += 1
            with open('show_category/words_training/article_categoryy_' + c + '.txt', 'w') as f:
                categories_link = soup.find(
                    class_='nav_color_' + str(index)).find('a')
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

        # 以下で分類器生成

        vocabulary = []
        n_cat = {}  # それぞれのカテゴリーの総単語数
        n_word = {}  # カテゴリー内における単語の生起回数
        for c in categories:
            words_training = get_words_from_text.get_words_from_text("file",
                'show_category/words_training/article_category_' + c + '.txt')
            n_word[c] = {}
            for word_training in words_training:
                vocabulary.append(word_training[0])
                n_word[c][word_training[0]] = word_training[1]
            n_cat[c] = sum(n_word[c].values())

        # 各カテゴリー毎の単語の生起確率
        p_word = {}
        for c in categories:
            p_word[c] = {}
            for word in vocabulary:
                if word in n_word[c]:
                    p_word[c][word] = (n_word[c][word] + 1) / (n_cat[c])

        with open('show_category/words_training_classification/vocabulary.dump', 'wb') as f:
            pickle.dump(vocabulary, f)
        with open('show_category/words_training_classification/word_possibility.dump', 'wb') as f:
            pickle.dump(p_word, f)
