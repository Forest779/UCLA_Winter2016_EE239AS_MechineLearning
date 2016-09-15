Run the code in this order:

source("deal_data.R");
source("group_for_cv.R");
source("linear_regression_network.R");
source("poly.R");
library("randomForest", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")
library("nnet", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library");
source("nnet.R");
source("cvpoly.R");
source("housingData.R");