from django.shortcuts import render_to_response
from django.template import loader
import urllib.request
from bs4 import BeautifulSoup
from show_category.forms import HpForm
from show_category import get_words_from_text
from show_category import classify

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
    test_list = list(get_words_from_text.get_words_from_text(
        "text", article_content))
    test_words = []
    for test_word in test_list:
        test_words.append(test_word[0])

    return render_to_response('results.html', {'category': classify.classify(test_words)})
