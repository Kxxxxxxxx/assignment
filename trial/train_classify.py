import math

# train_classify(ニュースカテゴリー,教師データ全単語,各教師データ,テストデータ)
def train_classify(categories, vocabulary, documents, data):

  # 各訓練文書の生起回数
  n_cls = {}
  total = 0.0
  for c in categories:
    n_cls[c] = len(documents[c])
    total += n_cls[c]

  # 各訓練文書の生起確率
  p_cls = {}
  for c in categories:
    p_cls[c] = n_cls[c] / total
  # print(vocabulary)
  # 各クラス毎の単語の生起回数
  n_word = {}
  for c in categories:
    n_word[c] = {}
    for d in documents[c]:
      count = 0
      for word in vocabulary:
        # print(d,word)
        if word == d:
          count += 1
          # print(count)
          n_word[c][word] = count

#各クラス毎の単語の生起確率
  p_word = {}
  for c in categories:
    p_word[c] = {}
    for word in vocabulary:
      if word in n_word[c]:
        p_word[c][word] = (n_word[c][word] + 1) / (n_cls[c])

  # 各クラス毎にlogP(D)を求める
  pp = {}
  for c in categories:
    pp[c] = math.log(p_cls[c])
    for word in vocabulary:
      if word in p_word[c]:
        if word in data:
          pp[c] += math.log(p_word[c][word])
        else:
          pp[c] += math.log((1 - p_word[c][word]))

 # 求めたlogP(D)の内、どれが最も大きいか判定
  for c in categories:
    maxpp = maxpp if 'maxpp' in locals() else pp[c]
    maxcls = maxcls if 'maxcls' in locals() else c

    if maxpp < pp[c]:
      maxpp = pp[c]
      maxcls =c

  return (maxcls)