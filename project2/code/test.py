# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 16:33:24 2016

@author: gudazhong
"""

from sklearn.decomposition import TruncatedSVD
from sklearn.random_projection import sparse_random_matrix
X = sparse_random_matrix(100, 100, density=0.1, random_state=42)
svd = TruncatedSVD(n_components=5, random_state=42)
svd.fit(X) 
X0 = X.toarray()
X1 = svd.transform(X)
