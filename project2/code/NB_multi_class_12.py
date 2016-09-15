# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 19:57:56 2016

@author: gudazhong
"""

from sklearn.naive_bayes import MultinomialNB
NB4_clf = MultinomialNB().fit(imfr_train_tfidf, imfr_train_target)
NB4_predicted = NB4_clf.predict(imfr_test_tfidf)

NB4_imfr_confusion = [[0,0,0,0],
                      [0,0,0,0],
                      [0,0,0,0],
                      [0,0,0,0]]
                  
for i in range(0,4*test_min_length):
    row = imfr_test_target[i]
    col = NB4_predicted[i]
    NB4_imfr_confusion[row][col] += 1
    
NB4_accuracy = (NB4_imfr_confusion[0][0] +
                NB4_imfr_confusion[1][1] + 
                NB4_imfr_confusion[2][2] + 
                NB4_imfr_confusion[3][3])/(4*test_min_length)
                
NB4_precision_i = NB4_imfr_confusion[0][0]/(NB4_imfr_confusion[0][0] + 
                                            NB4_imfr_confusion[1][0] + 
                                            NB4_imfr_confusion[2][0] + 
                                            NB4_imfr_confusion[3][0])
NB4_precision_m = NB4_imfr_confusion[1][1]/(NB4_imfr_confusion[0][1] + 
                                            NB4_imfr_confusion[1][1] + 
                                            NB4_imfr_confusion[2][1] + 
                                            NB4_imfr_confusion[3][1])
NB4_precision_f = NB4_imfr_confusion[2][2]/(NB4_imfr_confusion[0][2] + 
                                            NB4_imfr_confusion[1][2] + 
                                            NB4_imfr_confusion[2][2] + 
                                            NB4_imfr_confusion[3][2])
NB4_precision_r = NB4_imfr_confusion[3][3]/(NB4_imfr_confusion[0][3] + 
                                            NB4_imfr_confusion[1][3] + 
                                            NB4_imfr_confusion[2][3] + 
                                            NB4_imfr_confusion[3][3])

NB4_recall_i = NB4_imfr_confusion[0][0]/test_min_length
NB4_recall_m = NB4_imfr_confusion[1][1]/test_min_length
NB4_recall_f = NB4_imfr_confusion[2][2]/test_min_length
NB4_recall_r = NB4_imfr_confusion[3][3]/test_min_length