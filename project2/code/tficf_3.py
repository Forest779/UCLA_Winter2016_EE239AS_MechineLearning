# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 20:31:04 2016

@author: gudazhong
"""

train_class = []
test_class = []

for i in range(0,20):
    train_class.append('')
#    test_class.append('')
    
for i in range(0,20):
    for j in range(0,train_min_length):
        train_class[i] += train_doc[i][j]
#    for j in range(0,test_min_length):
#        test_class[i] += test_doc[i][j]


count_vect_train_cf = CountVectorizer(stop_words = stop_words)
X_train_counts_cf = count_vect_train_cf.fit_transform(train_class)
#count_vect_test_cf = CountVectorizer(stop_words = stop_words)
#X_test_counts_cf = count_vect_test_cf.fit_transform(test_class)


tficf_transformer_train = TfidfTransformer()
X_train_tficf = tficf_transformer_train.fit_transform(X_train_counts_cf)
#tficf_transformer_test = TfidfTransformer()
#X_test_tficf = tficf_transformer_test.fit_transform(X_test_counts_cf)


length_train_ificf = X_train_tficf.toarray().shape[1]
#length_test_ificf = X_test_tficf.toarray().shape[1]
num_train_important = []
#num_test_important = []

num_of_class = [2,3,8,9]
for i in num_of_class:
    temp_train = X_train_tficf.toarray()[i]
#    temp_test = X_test_tficf.toarray()[i]
    train_max_ten = sorted(temp_train, reverse = True)[9]
#    test_max_ten = sorted(temp_test, reverse = True)[9]
    
    temp_train_important = []
#    temp_test_important = []
    for j in range(0,length_train_ificf):
        if temp_train[j]>=train_max_ten:
            temp_train_important.append(j)
    num_train_important.append(temp_train_important)
#    for j in range(0,length_test_ificf):
#        if temp_test[j]>=test_max_ten:
#            temp_test_important.append(j)
#    num_test_important.append(temp_test_important)
    

term_train_important = []
#term_test_important = []
for i in range(0,4):
    term_train_important_temp = []
    for j in num_train_important[i]:
        term_train_important_temp.append(count_vect_train_cf.get_feature_names()[j])
    term_train_important.append(term_train_important_temp)
#    term_test_important_temp = []
#    for j in num_test_important[i]:
#        term_test_important_temp.append(count_vect_test_cf.get_feature_names()[j])
#    term_test_important.append(term_test_important_temp)
    


