# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 13:30:43 2016

@author: gudazhong
"""
from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components=50, random_state=42)
X_train_tfidf_small =  abs(svd.fit_transform(X_train_tfidf))
X_test_tfidf_small = abs(svd.transform(X_test_tfidf))


