house1 <- read.csv("data2.csv");
colnames(house1) <- c("CRIM","ZN","INDUS","CHAS","NOX","RM","AGE","DIS","RAD","TAX","PTRATIO","B","LSTAT","MEDV");


#------------------------------------------------
cdata <- house1;
length <- dim(cdata)[1];
randomRowNum <- sample(1:length);
groupRowNum <- list();
testDatah <- list();
trainDatah <- list();

for(i in 1:10) {
	groupRowNum[[i]] <- randomRowNum[(length/10*(i-1)+1):(length/10*i+1)];
}

for(i in 1:10) {
	testDatah[[i]] <- cdata[groupRowNum[[i]],];
	trainDatah[[i]] <- cdata[-groupRowNum[[i]],];
}


#------------------------------------------------
fith <- list();

for(i in 1:10) {
	fith[[i]] <- lm(trainDatah[[i]][,14] ~ trainDatah[[i]][,1] + 
		                                   trainDatah[[i]][,2] + 
		                                   trainDatah[[i]][,3] + 
		                                   trainDatah[[i]][,4] + 
		                                   trainDatah[[i]][,5] + 
		                                   trainDatah[[i]][,6] + 
		                                   trainDatah[[i]][,7] + 
		                                   trainDatah[[i]][,8] + 
		                                   trainDatah[[i]][,9] + 
		                                   trainDatah[[i]][,10] + 
		                                   trainDatah[[i]][,11] +
		                                   trainDatah[[i]][,12] + 
		                                   trainDatah[[i]][,13]);
}


#------------------------------------------------
RMSEh <- list();
RMSEhave <- 0;

for(i in 1:10) {
	RMSEh[[i]] <- sqrt(mean(fith[[i]][["residuals"]]^2));
	RMSEhave <- RMSEhave + RMSEh[[i]];
}

RMSEhave <- RMSEhave/10;


#------------------------------------------------
polymodelh <- list();
RMSEhp <- list();

for (i in 1:20) {
	n <- i;
	polymodelh[[i]] <- lm(MEDV ~ poly(CRIM,min(n,13)) + poly(ZN,min(n,15)) +
                        		poly(INDUS,min(n,15)) + poly(CHAS,1) +
                        		poly(NOX,min(n,15)) + poly(RM,n) +
                        		poly(AGE,n) + poly(DIS,min(n,15)) +
                        		poly(RAD,min(n,8)) + poly(TAX,min(n,15)) +
                        		poly(PTRATIO,min(n,15)) + poly(B,min(n,15)) +
                        		poly(LSTAT,min(n,15)), data=house1);
	RMSEhp[[i]] <- sqrt(mean(polymodelh[[i]][["residuals"]]^2));
}







