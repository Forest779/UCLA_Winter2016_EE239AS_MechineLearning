# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 16:11:36 2016

@author: gudazhong
"""

com_rec_train_tfidf = X_train_tfidf_small[0:8*377]
com_rec_test_tfidf = X_test_tfidf_small[0:8*251]

com_rec_train_target = []
for i in range (0,4*train_min_length):
    com_rec_train_target.append(0)
for i in range (0,4*train_min_length):
    com_rec_train_target.append(1)
    
com_rec_test_target = []
for i in range (0,4*test_min_length):
    com_rec_test_target.append(0)
for i in range (0,4*test_min_length):
    com_rec_test_target.append(1)
    
    
num_com = 4 * test_min_length
num_rec = 4 * test_min_length
num_total = num_com + num_rec