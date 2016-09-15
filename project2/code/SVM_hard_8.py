# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 12:06:44 2016

@author: gudazhong
"""
from sklearn.svm import SVC

SVM_hard_clf = SVC(class_weight = {0:1})
SVM_hard_clf.fit(com_rec_train_tfidf, com_rec_train_target)
SVM_hard_predicted = SVM_hard_clf.predict(com_rec_test_tfidf)
score = SVM_hard_clf.score(com_rec_test_tfidf,com_rec_test_target)

SVM_hard_com_to_rec = 0
SVM_hard_rec_to_com = 0
for i in range(0,test_min_length*8):
    if SVM_hard_predicted[i] - com_rec_test_target[i] == 1:
        SVM_hard_com_to_rec += 1
    if SVM_hard_predicted[i] - com_rec_test_target[i] == -1:
        SVM_hard_rec_to_com += 1
        
#set com to be the positive
SVM_hard_precision = (num_com - SVM_hard_com_to_rec)/(num_com + SVM_hard_rec_to_com - SVM_hard_com_to_rec)
SVM_hard_recall = (num_com - SVM_hard_com_to_rec)/num_com
SVM_hard_TPR = SVM_hard_recall
SVM_hard_FPR = SVM_hard_rec_to_com/num_rec
SVM_hard_accuracy = 1 - (SVM_hard_com_to_rec + SVM_hard_rec_to_com)/(num_total)

#       com   rec
# com
# rec
SVM_hard_confusion = [[num_com - SVM_hard_com_to_rec, SVM_hard_com_to_rec], [SVM_hard_rec_to_com, num_rec - SVM_hard_rec_to_com]]


SVM_hard_TPR_ROC = []
SVM_hard_FPR_ROC = []
for i in range (0,40):
    step = 0.000001/40*i
    threshold = 0.9999995 + step
    SVM_hard_clf_ROC = SVC(class_weight = {0:threshold} ).fit(com_rec_train_tfidf, com_rec_train_target)
    SVM_hard_predicted_ROC = SVM_hard_clf_ROC.predict(com_rec_test_tfidf)
    SVM_hard_com_to_rec_ROC = 0
    SVM_hard_rec_to_com_ROC = 0
    for j in range(0,test_min_length*8):
        if SVM_hard_predicted_ROC[j] - com_rec_test_target[j] == 1:
            SVM_hard_com_to_rec_ROC += 1
        if SVM_hard_predicted_ROC[j] - com_rec_test_target[j] == -1:
            SVM_hard_rec_to_com_ROC += 1
    SVM_hard_TPR_ROC.append((num_com - SVM_hard_com_to_rec_ROC)/num_com)
    SVM_hard_FPR_ROC.append(SVM_hard_rec_to_com_ROC/num_rec)

SVM_hard_TPR_ROC_list = SVM_hard_TPR_ROC
SVM_hard_FPR_ROC_list = SVM_hard_FPR_ROC
