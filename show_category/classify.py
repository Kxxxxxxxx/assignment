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

    # 求めたlogP(D)の内、どれが最も大きいか判定
    for c in p_word:
        max_pp = max_pp if 'max_pp' in locals() else pp[c]
        max_cat = max_cat if 'max_cat' in locals() else c

        if max_pp < pp[c]:
            max_pp = pp[c]
            max_cat = c

    return (max_cat)
