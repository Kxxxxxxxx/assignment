import math
import pickle

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
