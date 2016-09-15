n<-5;
length<-dim(trainData[[1]])[1];
polylist<-list();
RMSEploylist<-list();
for (i in 1:10) {
	polylist[[i]] <- lm(size ~ poly(week,n) + poly(day,min(n,6)) + poly(hour,min(n,5)) +
                     poly(flow,min(n,4)) + poly(file,n) + poly(btime,min(n,4)),
                     data=trainData[[i]])
	RMSEploylist[[i]]<-sqrt(sum(polylist[[i]][["residuals"]]^2)/length);
}