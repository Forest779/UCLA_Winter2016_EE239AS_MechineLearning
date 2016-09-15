# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 15:58:48 2016

@author: gudazhong
"""

from sklearn.datasets import fetch_20newsgroups
categories = [['comp.graphics'],
              ['comp.os.ms-windows.misc'],
              ['comp.sys.ibm.pc.hardware'],
              ['comp.sys.mac.hardware'],
              ['rec.autos'],
              ['rec.motorcycles'],
              ['rec.sport.baseball'],
              ['rec.sport.hockey'],
              ['misc.forsale'],
              ['soc.religion.christian'],
              ['alt.atheism'],
              ['comp.windows.x'],
              ['sci.crypt'],
              ['sci.electronics'],
              ['sci.med'],
              ['sci.space'],
              ['talk.politics.guns'],
              ['talk.politics.mideast'],
              ['talk.politics.misc'],
              ['talk.religion.misc']]
                     
train = []
test = []
train_length = []
test_length = []


for i in range(0,20):
    train.append(fetch_20newsgroups(subset='train', categories=categories[i], shuffle=True, random_state=42))
    test.append(fetch_20newsgroups(subset='test', categories=categories[i], shuffle=True, random_state=42))
    
for i in range(0,20):
    train_length.append(len(train[i].target))
    test_length.append(len(test[i].target))
    
computer_train_length = train_length[0] + train_length[1] + train_length[2] + train_length[3]
recreational_train_length = train_length[4] + train_length[5] + train_length[6] + train_length[7]
computer_test_length = test_length[0] + test_length[1] + test_length[2] + test_length[3]
recreational_test_length =  test_length[4] + test_length[5] + test_length[6] + test_length[7]


train_min_length = min(train_length)
test_min_length = min(test_length)


train_doc = []
test_doc = []
for i in range(0,20):
    train_doc.append(train[i].data[0:train_min_length]);
    test_doc.append(test[i].data[0:test_min_length]);


train_data = []
test_data = []
for i in range(0,20):
    for j in range(0,train_min_length):
        train_data.append(train_doc[i][j])
    for j in range(0,test_min_length):
        test_data.append(test_doc[i][j])
        
