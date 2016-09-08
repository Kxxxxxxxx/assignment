import MeCab
import collections
from machine_leaning_method_app import ngwords

mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')


def get_test_data(text):
    mecab.parse('')  # 文字列がGCされるのを防ぐ
    node = mecab.parseToNode(text)
    words = collections.Counter()
    while node:
        word = node.surface
        features = node.feature.split(",")
    # 品詞を取得
        pos = node.feature.split(",")[1]
    # print('{0} , {1}'.format(word, pos))
        if features[0] == "名詞" and node.surface not in ngwords.ng_noun:
            words[node.surface] += 1
        elif features[0] == "動詞" and features[6] not in ngwords.ng_verb:
            words[features[6]] += 1
        elif features[0] == "形容詞" and features[6] not in ngwords.ng_adjective:
            words[features[6]] += 1
    # 次の単語に進める
        node = node.next
    return words.most_common()
