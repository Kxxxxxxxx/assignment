from django.shortcuts import render_to_response
from django.template import loader
import urllib.request
from bs4 import BeautifulSoup
from show_category.forms import HpForm
import math
import pickle
import MeCab
import collections
from show_category import words_ng

def index(request):
    f = HpForm()
    return render_to_response('index.html', {'form1': f})

def results(request):
    response = urllib.request.urlopen(request.POST['address'])
    html = response.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    article_contents = soup.find(class_='article gtm-click').find_all('p')

    article_content = ''
    for article in article_contents:
        article_content += article.get_text()
    test_list = list(get_words_from_text(
        "text", article_content))
    test_words = []
    for test_word in test_list:
        test_words.append(test_word[0])

    return render_to_response('results.html', {'category': classify(test_words)})

def classify(data):

    with open('show_category/words_training_classification/word_possibility.dump', 'rb') as f:
        p_word = pickle.load(f)
    with open('show_category/words_training_classification/vocabulary.dump', 'rb') as f:
        vocabulary = pickle.load(f)
    
    # 各クラス毎にlogP(D)を求める
    pp = {}
    for c in p_word:
        pp[c] = math.log(1 / 8)
        for word in vocabulary:
            if word in data:
                pp[c] += math.log(p_word[c][word])

    max_cat = max([(v,k) for k,v in pp.items()])[1]

    return (max_cat)

def get_words_from_text(readin_variety, reading_content):
    if readin_variety == "file":
        with open(reading_content) as f:
            text = f.read()
    elif readin_variety == "text":
        text = reading_content

    mecab.parse('')  # 文字列がGCされるのを防ぐ
    node = mecab.parseToNode(text)
    words = collections.Counter()
    while node:
        word = node.surface
        features = node.feature.split(",")
        # 名詞:surface="スケート", feature="名詞,一般,*,*,*,*,スケート,スケート,スケート"
        # 動詞:surface="滑れ", feature="動詞,自立,*,*,一段,未然形,滑れる,スベレ,スベレ"
        pos = node.feature.split(",")[1]

        if features[0] == "名詞" and node.surface not in words_ng.ng_noun:
            words[node.surface] += 1
        elif features[0] == "動詞" and features[6] not in words_ng.ng_verb:
            words[features[6]] += 1
        elif features[0] == "形容詞" and features[6] not in words_ng.ng_adjective:
            words[features[6]] += 1
        node = node.next

    if readin_variety == "file":
        return words.most_common(300)
    elif readin_variety == "text":
        return words.most_common()
