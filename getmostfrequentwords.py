import MeCab
import collections
from trial import ngwords

mecab = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

def getmostfrequentwords(file):
    f = open(file)
    text = f.read()
    mecab.parse('')#文字列がGCされるのを防ぐ
    node = mecab.parseToNode(text)
    words = collections.Counter()
    while node:
     #単語を取得
        word = node.surface
        features = node.feature.split(",")
     #品詞を取得
        pos = node.feature.split(",")[1]
    # print('{0} , {1}'.format(word, pos))
        if features[0] == "名詞" and node.surface not in ngwords.ng_noun:
            words[node.surface] += 1
        elif features[0] == "動詞" and features[6] not in ngwords.ng_verb:
            words[features[6]] += 1
        elif features[0] == "形容詞" and features[6] not in ngwords.ng_adjective:
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
    return words.most_common(300)

# #
# for i in range(1,9):
#     print("category"+str(i))
#     mostFrequentWords("category"+str(i)+".txt")


