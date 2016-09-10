# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from show_category import get_words_from_text
from show_category import words_training
import urllib.request
from bs4 import BeautifulSoup
import pickle


class Command(BaseCommand):

    def handle(self, *args, **options):

        # 以下でグノシーから教師データに用いる記事を取得
        url = "https://gunosy.com/"
        response = urllib.request.urlopen(url)
        html = response.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        for i in range(1, 9):
            with open('show_category/words_training/article_categoryy' + str(i) + '.txt', 'w') as f:
                categories_link = soup.find(class_='nav_color_' + str(i)).find('a')
                categories_url = str(categories_link.get('href'))
                print(categories_url)
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
                        print(article_url)
                        for article in article_contents:
                            f.write(article.get_text())
                    response = urllib.request.urlopen(
                        categories_url + '?page=' + str(j))
                    html = response.read().decode("utf-8")
                    soup = BeautifulSoup(html, "html.parser")

        # 以下で分類器生成
        categories = ["entertainment", "sports", "fun", "domestic",
                      "abroad", "column", "it_science", "gourmet"]
        documents = {}
        vocabulary = []
        for i in range(1, 9):
            trainwords = get_words_from_text.get_words_from_text("file",
                                                                 'show_category/words_training/article_category' + str(i) + '.txt')
            wordslist = []
            for trainword in trainwords:
                wordslist.append(str(trainword[0]))
            vocabulary += wordslist
            documents[categories[i - 1]] = wordslist

        n_cls = {}
        total = 0.0
        for c in categories:
            n_cls[c] = len(documents[c])
            total += n_cls[c]

        # 各訓練文書の生起確率
        p_cls = {}
        for c in categories:
            p_cls[c] = n_cls[c] / total
        # 各クラス毎の単語の生起回数
        n_word = {}
        for c in categories:
            n_word[c] = {}
            for d in documents[c]:
                count = 0
                for word in vocabulary:
                    if word in d:
                        count += 1
                        n_word[c][word] = count

        # 各クラス毎の単語の生起確率
        p_word = {}
        for c in categories:
            p_word[c] = {}
            for word in vocabulary:
                if word in n_word[c]:
                    p_word[c][word] = (n_word[c][word] + 1) / (n_cls[c])

        with open('show_category/words_training_classification/vocabulary.dump', 'wb') as f:
            pickle.dump(vocabulary, f)
        with open('show_category/words_training_classification/word_possiblility.dump', 'wb') as f:
            pickle.dump(p_word, f)
