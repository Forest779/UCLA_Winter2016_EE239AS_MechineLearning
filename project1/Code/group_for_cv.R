cdata <- data2;
length <- dim(cdata)[1];
randomRowNum <- sample(1:length);
groupRowNum <- list();
testData <- list();
trainData <- list();

for(i in 1:10) {
	groupRowNum[[i]] <- randomRowNum[(length/10*(i-1)+1):(length/10*i+1)];
}

for(i in 1:10) {
	testData[[i]] <- cdata[groupRowNum[[i]],];
	trainData[[i]] <- cdata[-groupRowNum[[i]],];
}