import math
import pickle

# train_classify(ニュースカテゴリー,教師データ全単語,各教師データ,テストデータ)


def classify(data):

    with open('show_category/words_training_classification/word_possibility.dump', 'rb') as f:
        p_word = pickle.load(f)
    with open('show_category/words_training_classification/vocabulary.dump', 'rb') as f:
        vocabulary = pickle.load(f)
    # 各クラス毎にlogP(D)を求める
    pp = {}
    for c in p_word:
        print(c)
        pp[c] = math.log(1 / 8)
        for word in vocabulary:
            if word in p_word[c]:
                pp[c] += math.log(p_word[c][word])
    print(pp)

    # 求めたlogP(D)の内、どれが最も大きいか判定
    for c in p_word:
        maxpp = maxpp if 'maxpp' in locals() else pp[c]
        max_cat = max_cat if 'max_cat' in locals() else c

        if maxpp < pp[c]:
            maxpp = pp[c]
            max_cat = c

    return (max_cat)
