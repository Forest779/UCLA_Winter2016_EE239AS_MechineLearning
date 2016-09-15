# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 19:30:30 2016

@author: gudazhong
"""

#i is comp.sys.ibm.pc.hardware, m is comp.sys.mac.hardware, f is misc.forsale, r is soc.religion.christian

import numpy
imfr_train_tfidf = numpy.vstack([X_train_tfidf_small[2*train_min_length:3*train_min_length], 
                           X_train_tfidf_small[3*train_min_length:4*train_min_length], 
                           X_train_tfidf_small[8*train_min_length:9*train_min_length], 
                           X_train_tfidf_small[9*train_min_length:10*train_min_length]])
imfr_test_tfidf = numpy.vstack([X_test_tfidf_small[2*test_min_length:3*test_min_length], 
                          X_test_tfidf_small[3*test_min_length:4*test_min_length], 
                          X_test_tfidf_small[8*test_min_length:9*test_min_length], 
                          X_test_tfidf_small[9*test_min_length:10*test_min_length]])
imfr_train_target = []
for i in range(0,train_min_length):
    imfr_train_target.append(0)
for i in range(0,train_min_length):
    imfr_train_target.append(1)
for i in range(0,train_min_length):
    imfr_train_target.append(2)
for i in range(0,train_min_length):
    imfr_train_target.append(3)

imfr_test_target = []
for i in range(0,test_min_length):
    imfr_test_target.append(0)
for i in range(0,test_min_length):
    imfr_test_target.append(1)
for i in range(0,test_min_length):
    imfr_test_target.append(2)
for i in range(0,test_min_length):
    imfr_test_target.append(3)