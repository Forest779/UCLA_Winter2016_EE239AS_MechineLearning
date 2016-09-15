# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 12:25:21 2016

@author: gudazhong
"""

from sklearn.svm import SVC
SVM_ovo_clf = SVC(C = 0.5)
SVM_ovo_clf.fit(imfr_train_tfidf, imfr_train_target)
SVM_ovo_predicted = SVM_ovo_clf.predict((imfr_test_tfidf))


SVM_ovo_imfr_confusion = [[0,0,0,0],
                          [0,0,0,0],
                          [0,0,0,0],
                          [0,0,0,0]]

for i in range(0,4*test_min_length):
    row = imfr_test_target[i]
    col = SVM_ovo_predicted[i]
    SVM_ovo_imfr_confusion[row][col] += 1
    
SVM_ovo_accuracy = (SVM_ovo_imfr_confusion[0][0] +
                    SVM_ovo_imfr_confusion[1][1] + 
                    SVM_ovo_imfr_confusion[2][2] + 
                    SVM_ovo_imfr_confusion[3][3])/(4*test_min_length)
                    
SVM_ovo_precision_i = SVM_ovo_imfr_confusion[0][0]/(SVM_ovo_imfr_confusion[0][0] + 
                                                   SVM_ovo_imfr_confusion[1][0] + 
                                                   SVM_ovo_imfr_confusion[2][0] + 
                                                   SVM_ovo_imfr_confusion[3][0])
SVM_ovo_precision_m = SVM_ovo_imfr_confusion[1][1]/(SVM_ovo_imfr_confusion[0][1] + 
                                                    SVM_ovo_imfr_confusion[1][1] + 
                                                    SVM_ovo_imfr_confusion[2][1] + 
                                                    SVM_ovo_imfr_confusion[3][1])
SVM_ovo_precision_f = SVM_ovo_imfr_confusion[2][2]/(SVM_ovo_imfr_confusion[0][2] + 
                                                    SVM_ovo_imfr_confusion[1][2] + 
                                                    SVM_ovo_imfr_confusion[2][2] + 
                                                    SVM_ovo_imfr_confusion[3][2])
SVM_ovo_precision_r = SVM_ovo_imfr_confusion[3][3]/(SVM_ovo_imfr_confusion[0][3] + 
                                                    SVM_ovo_imfr_confusion[1][3] + 
                                                    SVM_ovo_imfr_confusion[2][3] + 
                                                    SVM_ovo_imfr_confusion[3][3])

SVM_ovo_recall_i = SVM_ovo_imfr_confusion[0][0]/test_min_length
SVM_ovo_recall_m = SVM_ovo_imfr_confusion[1][1]/test_min_length
SVM_ovo_recall_f = SVM_ovo_imfr_confusion[2][2]/test_min_length
SVM_ovo_recall_r = SVM_ovo_imfr_confusion[3][3]/test_min_length