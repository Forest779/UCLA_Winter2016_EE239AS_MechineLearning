# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 16:47:35 2016

@author: gudazhong
"""
from numpy import *

cv5_half_length = 300
cv5_length = cv5_half_length*2
cv5_data = []
for i in range(0,5):
    cv5_data.append(numpy.vstack((com_rec_train_tfidf[i*cv5_half_length : (i+1)*cv5_half_length], 
                                  com_rec_train_tfidf[4*train_min_length + i*cv5_half_length : 
                                                      4*train_min_length + (i+1)*cv5_half_length])))
    #cv5_data.append(com_rec_train_tfidf[4*train_min_length + i*cv5_half_length : 4*train_min_length + (i+1)*cv5_half_length])
    

cv5_train = []
cv5_test = []  
for i in range(0,5):
    cv5_test.append(cv5_data[i])
    temp = []
    for j in range (0,5):
        if j!=i:
            for k in range (0,cv5_length):
                temp.append(cv5_data[j][k])
    cv5_train.append(numpy.array(temp))
            
        
cv5_train_target = []
cv5_test_target = []

for i in range (0,300):
    cv5_test_target.append(0)
for i in range (0,300):
    cv5_test_target.append(1)
    
for i in range (0,4):
    for j in range (0,300):
        cv5_train_target.append(0)
    for j in range (0,300):
        cv5_train_target.append(1)
    

