from django.shortcuts import render_to_response
from django.template import loader
import urllib.request
from bs4 import BeautifulSoup
from trial.forms import HpForm
from trial import get_traindata
from trial.get_testdata import *
from trial.train_classify import *

# Create your views here.

def index(request):
	f = HpForm()
	return render_to_response('index.html',{'form1':f})

def results(request):
#フォームに入力されたグノシーの記事から本文部分を抜き取り単語に分解する。
	response = urllib.request.urlopen(request.POST['address'])
	html = response.read().decode("utf-8")
	soup = BeautifulSoup(html, "html.parser")
	article_contents = soup.find(class_='article gtm-click').find_all('p')

	article_content = ''
	for article in article_contents:
		article_content += article.get_text()
	testlist = list(get_testdata(article_content))
	testwords = []
	for testword in testlist:
		testwords += str(testword[0])
	vocabulary = get_traindata.vocabulary
	dict = get_traindata.dict
	categories = get_traindata.categories

	return render_to_response('results.html',{'category':train_classify(categories, vocabulary, dict, testwords)})


