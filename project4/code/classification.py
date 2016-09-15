# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 19:02:21 2016

@author: gudazhong
"""

import json
data = []
i=0
with open('./tweet_data/tweets_#gohawks.txt', encoding='utf-8') as fin:
    for line in fin:
        if i<1000:
            data.append(json.loads(line))
            i = i + 1
        if i>1000:
            break
    fin.close()

i=0
with open('./tweet_data/tweets_#gopatriots.txt', encoding='utf-8') as fin:
    for line in fin:
        if i<1000:
            data.append(json.loads(line))
            i = i + 1
        if i>1000:
            break
    fin.close()
    
i=0
with open('./tweet_data/tweets_#nfl.txt', encoding='utf-8') as fin:
    for line in fin:
        if i<1000:
            data.append(json.loads(line))
            i = i + 1
        if i>1000:
            break
    fin.close()
    
i=0
with open('./tweet_data/tweets_#patriots.txt', encoding='utf-8') as fin:
    for line in fin:
        if i<1000:
            data.append(json.loads(line))
            i = i + 1
        if i>1000:
            break
    fin.close()
    
i=0
with open('./tweet_data/tweets_#sb49.txt', encoding='utf-8') as fin:
    for line in fin:
        if i<1000:
            data.append(json.loads(line))
            i = i + 1
        if i>1000:
            break
    fin.close()
    
i=0
with open('./tweet_data/tweets_#superbowl.txt', encoding='utf-8') as fin:
    for line in fin:
        if i<1000:
            data.append(json.loads(line))
            i = i + 1
        if i>1000:
            break
    fin.close()
    
i=0
content=[]
tag=[]
for i in range (0,6000):
    content.append(data[i]['tweet']['text'])
    tag.append(i//1000)    
    
from sklearn.feature_extraction import text
stop_words = text.ENGLISH_STOP_WORDS

from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer(stop_words = stop_words)

counts = count_vect.fit_transform(content)

from sklearn.feature_extraction.text import TfidfTransformer

tfidf_transformer = TfidfTransformer()
tfidf = tfidf_transformer.fit_transform(counts)

from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components=50, random_state=42)
tfidf_small =  abs(svd.fit_transform(tfidf))


from sklearn.naive_bayes import MultinomialNB
NB4_clf = MultinomialNB().fit(tfidf_small, tag)
NB4_predicted = NB4_clf.predict(tfidf_small)




NB4_confusion = [[0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0]]
                  
for i in range(0,6000):
    row = tag[i]
    col = NB4_predicted[i]
    NB4_confusion[row][col] += 1
    
NB4_accuracy = (NB4_confusion[0][0] +
                NB4_confusion[1][1] + 
                NB4_confusion[2][2] + 
                NB4_confusion[3][3] +
                NB4_confusion[4][4] +
                NB4_confusion[5][5])/6000
                
NB4_precision = NB4_confusion[0][0]/(NB4_confusion[0][0] + 
                                     NB4_confusion[1][0] + 
                                     NB4_confusion[2][0] + 
                                     NB4_confusion[3][0] + 
                                     NB4_confusion[4][0] + 
                                     NB4_confusion[5][0]) 
                   
NB4_recall = NB4_confusion[0][0]/1000                        


print(tfidf.shape)