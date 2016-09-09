import showcategory.testwords
# 以下カテゴリーごとに得られた単語をテキストファイルで読み込む
categories = ["entertainment", "sports", "fun", "domestic",
              "abroad", "column", "it_science", "gourmet"]
dict = {}
vocabulary = []
for i in range(1, 9):
    f = open("showcategory/testwords/testwords_category" +
             str(i) + ".txt", "r")
    words = f.readlines()
    wordslist = []
    for word in words:
        word = word.split("\n")
        wordslist.append(word[0])
    f.close()
    vocabulary += wordslist
    dict[categories[i - 1]] = wordslist
