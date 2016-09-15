testLength <- dim(cdata)[1]/10;
y <- list();
X <- list();
X1 <- list();
RMSE <- list();
error <- list();
beta <- list();

for(i in 1:10) {
	y[[i]] <- testData[[i]][,6];
	X1[[i]] <- testData[[i]][,-6];
	X[[i]] <- X1[[i]][,-4];
	beta[[i]] <- fit[[i]][[1]][-1];
	error[[i]] <- y[[i]]-X[[i]]%*%beta[[i]]-fit[[i]][[1]][1];
	RMSE[[i]] <- sqrt(sum(error[[i]]^2)/length(error[[i]]));
}

RMSEAve <- 0;
for(i in 1:10) RMSEAve <- RMSEAve+RMSE[[i]];
RMSEAve <- RMSEAve/10;