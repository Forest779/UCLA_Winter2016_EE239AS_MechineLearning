n<-4;
polymodel <- lm(size ~ poly(week,n) + poly(day,min(n,6)) + poly(hour,min(n,5)) +
                poly(flow,min(n,4)) + poly(file,n) + poly(btime,min(n,4)),
                data=data2)
result<-data.frame(fitted(polymodel));
pre<-data.frame(predict(polymodel,newdata=data2));
sqrt(sum(polymodel[["residuals"]]^2)/18588);