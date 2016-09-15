# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 19:18:05 2016

@author: gudazhong
"""

from sklearn.linear_model import LogisticRegression
LR_clf = LogisticRegression(class_weight = {0:1} )
LR_clf.fit(com_rec_train_tfidf, com_rec_train_target)
LR_predicted = LR_clf.predict(com_rec_test_tfidf)

LR_com_to_rec = 0
LR_rec_to_com = 0
for i in range(0,test_min_length*8):
    if LR_predicted[i] - com_rec_test_target[i] == 1:
        LR_com_to_rec += 1
    if LR_predicted[i] - com_rec_test_target[i] == -1:
        LR_rec_to_com += 1
        
#set com to be the positive
LR_precision = (num_com - LR_com_to_rec)/(num_com + LR_rec_to_com - LR_com_to_rec)
LR_recall = (num_com - LR_com_to_rec)/num_com
LR_TPR = LR_recall
LR_FPR = LR_rec_to_com/num_rec
LR_accuracy = 1 - (LR_com_to_rec + LR_rec_to_com)/(num_total)

#       com   rec
# com
# rec
LR_confusion = [[num_com - LR_com_to_rec, LR_com_to_rec], [LR_rec_to_com, num_rec - LR_rec_to_com]]



LR_TPR_ROC = []
LR_FPR_ROC = []
for i in range (0,40):
    step = 1/40*i
    threshold = 0.5 + step
    LR_clf_ROC = LogisticRegression(class_weight = {0:threshold} ).fit(com_rec_train_tfidf, com_rec_train_target)
    LR_predicted_ROC = LR_clf_ROC.predict(com_rec_test_tfidf)
    LR_com_to_rec_ROC = 0
    LR_rec_to_com_ROC = 0
    for j in range(0,test_min_length*8):
        if LR_predicted_ROC[j] - com_rec_test_target[j] == 1:
            LR_com_to_rec_ROC += 1
        if LR_predicted_ROC[j] - com_rec_test_target[j] == -1:
            LR_rec_to_com_ROC += 1
    LR_TPR_ROC.append((num_com - LR_com_to_rec_ROC)/num_com)
    LR_FPR_ROC.append(LR_rec_to_com_ROC/num_rec)

LR_TPR_ROC_list = LR_TPR_ROC
LR_FPR_ROC_list = LR_FPR_ROC