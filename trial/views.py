from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import loader
from trial.forms import HpForm
import urllib.request
import collections
from bs4 import BeautifulSoup
import MeCab
import trial
import math
# Create your views here.
def index(request):
	# if request.method == 'POST':
		# f = HpForm(request.POST)
	# else:
	f = HpForm()
	return render_to_response('index.html',{'form1':f})
	# return HttpResponse(f.as_table())
	# template = loader.get_template('polls/index.html')
    # return HttpResponse("Hello, world. You're at the polls index.")


def results(request):
	#フォームに入力されたグノシーの記事から本文部分を抜き取り単語に分解する。
	response = urllib.request.urlopen(request.POST["adress"])
	html = response.read().decode("utf-8")
	soup = BeautifulSoup(html, "html.parser")
	article_contents = soup.find(class_='article gtm-click').find_all('p')
			
			# print(article_url)
	article_content = ''
	testwords = []
	for article in article_contents:
		article_content += article.get_text()
	testlist = list(WordsFromSites(article_content))
	for x in testlist:
		testwords += str(x[0])

	#以下カテゴリーごとに得られた単語をテキストファイルで読み込む
	dict ={}
	f = open("trial/output_category1.txt","r")
	word = f.readlines()
	a = []
	for line in word:
		line = line.split("\n")
		a.append(line[0])
	f.close()
	dict["entertainment"] = a
	f = open("trial/output_category2.txt","r")
	word = f.readlines()
	a = []
	for line in word:
  		line = line.split("\n")
  		a.append(line[0])
	f.close()
	dict["sports"] = a
	f = open("trial/output_category3.txt","r")
	word = f.readlines()
	a = []
	for line in word:
		line = line.split("\n")
		a.append(line[0])
	f.close()
	dict["fun"] = a
	f = open("trial/output_category4.txt","r")
	word = f.readlines()
	a = []
	for line in word:
		line = line.split("\n")
		a.append(line[0])
	f.close()
	dict["domestic"] = a
	f = open("trial/output_category5.txt","r")
	word = f.readlines()
	a = []
	for line in word:
		line = line.split("\n")
		a.append(line[0])
	f.close()
	dict["abroad"] = a
	f = open("trial/output_category6.txt","r")
	word = f.readlines()
	a = []
	for line in word:
		line = line.split("\n")
		a.append(line[0])
	f.close()
	dict["column"] = a
	f = open("trial/output_category7.txt","r")
	word = f.readlines()
	a = []
	for line in word:
		line = line.split("\n")
		a.append(line[0])
	f.close()
	dict["it_science"] = a
	f = open("trial/output_category8.txt","r")
	word = f.readlines()
	a = []
	for line in word:
		line = line.split("\n")
		a.append(line[0])
	f.close()
	dict["gourmet"] = a
# f = open("output_allcategory.dat","r")
# word = f.readlines()
# a = []
# for line in word:
#   line = line.split("\n")
#   a.append(line[0])
# f.close()
# dict["vocabulary"] = a
	f = open("trial/output_allcategory.txt","r")
	word = f.readlines()
	a = []
	for line in word:
		line = line.split("\n")
		a.append(line[0])
	f.close()
	vocabulary = a
	cls = ["entertainment","sports","fun","domestic","abroad","column","it_science","gourmet"]

	# return HttpResponse(train_classify(cls, vocabulary, dict, trainwords))
	#	train_classify(カテゴリー,全単語,各教師データ,テストデータ)
	return render_to_response('results.html',{'category':train_classify(cls, vocabulary, dict, testwords)})


	#以下MeCabを使用するための関数とカテゴリー判定のための関数

def WordsFromSites(text):
	mecab = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
	mecab.parse('')#文字列がGCされるのを防ぐ
	node = mecab.parseToNode(text)
	words = collections.Counter()
	ng_noun = ["こと", "の", "もの", "それ", "とき", "、", "､", "。", "｡", "(", ")", ".","１","２","３","４","５","６","７","８","９"]
	ng_verb = ["する", "いる", "なる", "ある", "れる","られる","できる"]
	ng_adjective = ["よう"]
	while node:
	#単語を取得
		word = node.surface
		features = node.feature.split(",")
	#品詞を取得
		pos = node.feature.split(",")[1]
    # print('{0} , {1}'.format(word, pos))
		if features[0] == "名詞" and node.surface not in ng_noun:
			words[node.surface] += 1
		elif features[0] == "動詞" and features[6] not in ng_verb:
			words[features[6]] += 1
		elif features[0] == "形容詞" and features[6] not in ng_adjective:
			words[features[6]] += 1
    #次の単語に進める
		node = node.next
    # 名詞:surface="スケート", feature="名詞,一般,*,*,*,*,スケート,スケート,スケート"
    # 動詞:surface="滑れ", feature="動詞,自立,*,*,一段,未然形,滑れる,スベレ,スベレ"
    # print(words.most_common(100))
    # for vocas in words.most_common(100):
    #     print(vocas[0])
        # for voca in vocas:
        #     print (voca)
	return words.most_common()

def mostFrequentWords(file):
    f = open(file)
    text = f.read()
    mecab.parse('')#文字列がGCされるのを防ぐ
    node = mecab.parseToNode(text)
    words = collections.Counter()
    ng_noun = ["こと", "の", "もの", "それ", "とき", "、", "､", "。", "｡", "(", ")", ".","１","２","３","４","５","６","７","８","９"]
    ng_verb = ["する", "いる", "なる", "ある", "れる","られる","できる"]
    ng_adjective = ["よう"]
    while node:
     #単語を取得
        word = node.surface
        features = node.feature.split(",")
     #品詞を取得
        pos = node.feature.split(",")[1]
    # print('{0} , {1}'.format(word, pos))
        if features[0] == "名詞" and node.surface not in ng_noun:
            words[node.surface] += 1
        elif features[0] == "動詞" and features[6] not in ng_verb:
            words[features[6]] += 1
        elif features[0] == "形容詞" and features[6] not in ng_adjective:
            words[features[6]] += 1
    #次の単語に進める
        node = node.next
    # 名詞:surface="スケート", feature="名詞,一般,*,*,*,*,スケート,スケート,スケート"
    # 動詞:surface="滑れ", feature="動詞,自立,*,*,一段,未然形,滑れる,スベレ,スベレ"
    # print(words.most_common(100))
    # for vocas in words.most_common(100):
    #     print(vocas[0])
        # for voca in vocas:
        #     print (voca)
    return words.most_common(200)

def WordsOfText(file):
    f = open(file)
    text = f.read()
    mecab.parse('')#文字列がGCされるのを防ぐ
    node = mecab.parseToNode(text)
    words = collections.Counter()
    ng_noun = ["こと", "の", "もの", "それ", "とき", "、", "､", "。", "｡", "(", ")", ".","１","２","３","４","５","６","７","８","９"]
    ng_verb = ["する", "いる", "なる", "ある", "れる","られる","できる"]
    ng_adjective = ["よう"]
    while node:
     #単語を取得
        word = node.surface
        features = node.feature.split(",")
     #品詞を取得
        pos = node.feature.split(",")[1]
    # print('{0} , {1}'.format(word, pos))
        if features[0] == "名詞" and node.surface not in ng_noun:
            words[node.surface] += 1
        elif features[0] == "動詞" and features[6] not in ng_verb:
            words[features[6]] += 1
        elif features[0] == "形容詞" and features[6] not in ng_adjective:
            words[features[6]] += 1
    #次の単語に進める
        node = node.next
    # 名詞:surface="スケート", feature="名詞,一般,*,*,*,*,スケート,スケート,スケート"
    # 動詞:surface="滑れ", feature="動詞,自立,*,*,一段,未然形,滑れる,スベレ,スベレ"
    # print(words.most_common(100))
    # for vocas in words.most_common(100):
    #     print(vocas[0])
        # for voca in vocas:
        #     print (voca)
    return words.most_common()


    #訓練データを教師データにかけてカテゴリーを判定する
def train_classify(cls, vocabulary, documents, data):

  # 各訓練文書の生起回数
  n_cls = {}
  total = 0.0
  for c in cls:
    n_cls[c] = len(documents[c])
    total += n_cls[c]

  # 各訓練文書の生起確率
  p_cls = {}
  for c in cls:
    p_cls[c] = n_cls[c] / total
  # print(vocabulary)
  # 各クラス毎の単語の生起回数
  n_word = {}
  for c in cls:
    n_word[c] = {}
    for d in documents[c]:
      count = 0
      for word in vocabulary:
        # print(d,word)
        if word == d:
          count += 1
          # print(count)
          n_word[c][word] = count
          # print(n_word[c][word])

#各クラス毎の単語の生起確率
  p_word = {}
  for c in cls:
    p_word[c] = {}
    for word in vocabulary:
      if word in n_word[c]:
        p_word[c][word] = (n_word[c][word] + 1) / (n_cls[c])
        # print(p_word[c][word])

  # 各クラス毎にlogP(D)を求める
  pp = {}
  for c in cls:
    # print(p_cls[c])
    pp[c] = math.log(p_cls[c])
    for word in vocabulary:
      if word in p_word[c]:
        if word in data:
          pp[c] += math.log(p_word[c][word])
        else:
          pp[c] += math.log((1 - p_word[c][word]))

 # 求めたlogP(D)の内、どれが最も大きいか判定
  for c in cls:
    # print(pp[c])
    maxpp = maxpp if 'maxpp' in locals() else pp[c]
    maxcls = maxcls if 'maxcls' in locals() else c

    if maxpp < pp[c]:
      maxpp = pp[c]
      maxcls =c

  return maxcls