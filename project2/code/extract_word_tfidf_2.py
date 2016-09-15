# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 19:04:24 2016

@author: gudazhong
"""
from sklearn.feature_extraction import text
stop_words = text.ENGLISH_STOP_WORDS


from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer(stop_words = stop_words)
X_train_counts = count_vect.fit_transform(train_data)
X_test_counts = count_vect.transform(test_data)




from sklearn.feature_extraction.text import TfidfTransformer

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
X_test_tfidf = tfidf_transformer.transform(X_test_counts)

origin_term_num = X_train_counts.shape[1]