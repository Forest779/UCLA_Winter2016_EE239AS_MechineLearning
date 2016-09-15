# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 16:45:04 2016

@author: gudazhong
"""
from sklearn.naive_bayes import MultinomialNB
NB2_clf = MultinomialNB(class_prior = [1,1]).fit(com_rec_train_tfidf, com_rec_train_target)
NB2_predicted = NB2_clf.predict(com_rec_test_tfidf)

NB2_com_to_rec = 0
NB2_rec_to_com = 0
for i in range(0,test_min_length*8):
    if NB2_predicted[i] - com_rec_test_target[i] == 1:
        NB2_com_to_rec += 1
    if NB2_predicted[i] - com_rec_test_target[i] == -1:
        NB2_rec_to_com += 1


#set com to be the positive
NB2_precision_com = (num_com - NB2_com_to_rec)/(num_com + NB2_rec_to_com - NB2_com_to_rec)
NB2_recall_com = (num_com - NB2_com_to_rec)/num_com
NB2_precision_rec = (num_rec - NB2_rec_to_com)/(num_rec + NB2_com_to_rec - NB2_rec_to_com)
NB2_recall_rec = (num_rec - NB2_rec_to_com)/num_rec
NB2_TPR = NB2_recall_com
NB2_FPR = NB2_rec_to_com/num_rec
NB2_accuracy = 1 - (NB2_com_to_rec + NB2_rec_to_com)/(num_total)

#       com   rec
# com
# rec
NB2_confusion = [[num_com - NB2_com_to_rec, NB2_com_to_rec], [NB2_rec_to_com, num_rec - NB2_rec_to_com]]



#Use NB2_TPR_ROC and NB2_FPR_ROC to plot the ROC
NB2_TPR_ROC = []
NB2_FPR_ROC = []
for i in range (0,40):
    step = 0.2/40*i
    threshold = 0.9 + step
    NB2_clf_ROC = MultinomialNB(class_prior = [threshold,1]).fit(com_rec_train_tfidf, com_rec_train_target)
    NB2_predicted_ROC = NB2_clf_ROC.predict(com_rec_test_tfidf)
    NB2_com_to_rec_ROC = 0
    NB2_rec_to_com_ROC = 0
    for j in range(0,test_min_length*8):
        if NB2_predicted_ROC[j] - com_rec_test_target[j] == 1:
            NB2_com_to_rec_ROC += 1
        if NB2_predicted_ROC[j] - com_rec_test_target[j] == -1:
            NB2_rec_to_com_ROC += 1
    NB2_TPR_ROC.append((num_com - NB2_com_to_rec_ROC)/num_com)
    NB2_FPR_ROC.append(NB2_rec_to_com_ROC/num_rec)
    
NB2_TPR_ROC_list = NB2_TPR_ROC
NB2_FPR_ROC_list = NB2_FPR_ROC 
