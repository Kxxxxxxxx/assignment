from django.shortcuts import render_to_response
from django.template import loader
import urllib.request
from bs4 import BeautifulSoup
from machine_leaning_method_app.forms import HpForm
from machine_leaning_method_app import get_train_data
from machine_leaning_method_app.get_test_data import *
from machine_leaning_method_app.train_classify import *

# Create your views here.


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
    testlist = list(get_test_data(article_content))
    testwords = []
    for testword in testlist:
        testwords += str(testword[0])
    categories = get_train_data.categories
    vocabulary = get_train_data.vocabulary
    dict = get_train_data.dict

    return render_to_response('results.html', {'category': train_classify(categories, vocabulary, dict, testwords)})
