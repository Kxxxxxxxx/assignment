# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from show_category import views
import urllib.request
import pickle
from show_category import categories_classification
import MeCab

class Command(BaseCommand):

    def handle(self, *args, **options):
        # 以下で分類器生成
        vocabulary = []
        n_cat = {}  # それぞれのカテゴリーの総単語数
        n_word = {}  # カテゴリー内における単語の生起回数
        words_in_category = {}  # それぞれのカテゴリーに属する単語を格納
        categories = categories_classification.categories_classification
        for c in categories:
            words_training = views.get_words_from_text("file",
                'show_category/words_training/article_category_' + c + '.txt')
            n_word[c] = {}
            words_list = []
            for word_training in words_training:
                words_list.append(word_training[0])
                vocabulary.append(word_training[0])
                n_word[c][word_training[0]] = word_training[1]
            n_cat[c] = sum(n_word[c].values())
            words_in_category[c] = words_list
        for c in categories:
            for word in vocabulary:
                if word not in words_in_category[c]:
                    n_word[c][word] = 0

        # 各カテゴリー毎の単語の生起確率
        p_word = {}
        for c in categories:
            p_word[c] = {}
            for word in vocabulary:
                p_word[c][word] = (n_word[c][word] + 1) / (n_cat[c])

        with open('show_category/words_training_classification/vocabulary.dump', 'wb') as f:
            pickle.dump(vocabulary, f)
        with open('show_category/words_training_classification/word_possibility.dump', 'wb') as f:
            pickle.dump(p_word, f)
