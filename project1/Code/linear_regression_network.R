fit <- list();

for(i in 1:10) {
	fit[[i]] <- lm(trainData[[i]][,6] ~ 
		                             trainData[[i]][,1]+
		                        	 trainData[[i]][,2]+
		                             trainData[[i]][,3]+
		                        	 trainData[[i]][,5]+
		                        	 trainData[[i]][,7]);
}




