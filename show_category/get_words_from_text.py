import MeCab
import collections
from show_category import words_ng

mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')


def get_words_from_text(readin_variety, reading_content):
    if readin_variety == "file":
        f = open(reading_content)
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
