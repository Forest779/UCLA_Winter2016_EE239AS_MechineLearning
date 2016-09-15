data2.neu <- nnet(size~. , data=data2 , size=20, maxit=1000 , decay=5e-4);
RMSE.neu <- sqrt(mean(data2.neu$residuals^2));
print(RMSE.neu);
