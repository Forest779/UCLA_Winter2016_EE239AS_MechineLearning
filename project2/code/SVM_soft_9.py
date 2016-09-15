# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 12:07:22 2016

@author: gudazhong
"""
from sklearn.svm import SVC

SVM_soft_ave_accuracy = []
SVM_soft_ave_precision = []
SVM_soft_ave_recall = []
SVM_soft_ave_confusion = []

margin = [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000]
for i in margin:
    SVM_soft_clf = []
    SVM_soft_com_to_rec = []
    SVM_soft_rec_to_com = []
    SVM_soft_predicted = []
    SVM_soft_accuracy = []
    SVM_soft_precision = []
    SVM_soft_recall = []
    SVM_soft_confusion = []
    
    for j in range(0,5):
        SVM_soft_clf.append(SVC(C = i))
        SVM_soft_clf[j].fit(cv5_train[j],cv5_train_target)
        SVM_soft_predicted.append(SVM_soft_clf[j].predict(cv5_test[j])) 
        
        SVM_soft_com_to_rec.append(0)
        SVM_soft_rec_to_com.append(0)
        for k in range(0, cv5_length):
            if SVM_soft_predicted[j][k] - cv5_test_target[k] == 1:
                SVM_soft_com_to_rec[j] += 1
            if SVM_soft_predicted[j][k] - cv5_test_target[k] == -1:
                SVM_soft_rec_to_com[j] += 1
        SVM_soft_precision.append((cv5_half_length - SVM_soft_com_to_rec[j])/(cv5_half_length + SVM_soft_rec_to_com[j] - SVM_soft_com_to_rec[j]))
        SVM_soft_recall.append((cv5_half_length - SVM_soft_com_to_rec[j])/cv5_half_length)
        SVM_soft_accuracy.append(1 - (SVM_soft_com_to_rec[j] + SVM_soft_rec_to_com[j])/(cv5_length))
        SVM_soft_confusion.append([[cv5_half_length - SVM_soft_com_to_rec[j], SVM_soft_com_to_rec[j]], 
                                   [SVM_soft_rec_to_com[j], cv5_half_length - SVM_soft_rec_to_com[j]]])

    
    
    
    temp_ave_accuracy = 0
    temp_ave_precision = 0
    temp_ave_recall = 0
    temp_ave_confusion =  [[0,0],[0,0]]
    for j in range(0,5):
        temp_ave_accuracy += SVM_soft_accuracy[j]
        temp_ave_precision += SVM_soft_precision[j]
        temp_ave_recall += SVM_soft_recall[j]
        temp_ave_confusion[0][0] += SVM_soft_confusion[j][0][0]
        temp_ave_confusion[0][1] += SVM_soft_confusion[j][0][1]
        temp_ave_confusion[1][0] += SVM_soft_confusion[j][1][0]
        temp_ave_confusion[1][1] += SVM_soft_confusion[j][1][1]
    temp_ave_confusion[0][0] = temp_ave_confusion[0][0]/5
    temp_ave_confusion[0][1] = temp_ave_confusion[0][1]/5
    temp_ave_confusion[1][0] = temp_ave_confusion[1][0]/5
    temp_ave_confusion[1][1] = temp_ave_confusion[1][1]/5
    SVM_soft_ave_accuracy.append(temp_ave_accuracy/5)
    SVM_soft_ave_precision.append(temp_ave_precision/5)
    SVM_soft_ave_recall.append(temp_ave_recall/5)
    SVM_soft_ave_confusion.append(temp_ave_confusion)

