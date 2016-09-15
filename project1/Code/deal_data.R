#data1 is the origin data.
#data2 is the data transfered into numbers.
#data3 is the data which we transfer week,day,hours in hours.
#data4 is the result of sort of data3 by time.
#workflow is the list of data4 seprated into each workflow.
#workflowSum is the list that we add the size of all files in each time point
#            which has 5 component.
#totalflowSum is the size of all files in each time point, not seprated in workflow
#            which has 5 component.


#------------------------------------------------------------------


setwd("/Users/gudazhong/R/239p1");
data1=read.csv("data1.csv");
length=length(data1[,1]);
weekMax=15;
hourMax=21;
timePeriod=4;
timeLength=((weekMax-1)*7*24+6*24+21-1)/timePeriod+1;


#------------------------------------------------------------------


data2=matrix(nrow=length,ncol=7);
for(i in 1:length) {
	data2[i,1]=data1[i,1];
	data2[i,3]=data1[i,3];
	data2[i,6]=data1[i,6];
	data2[i,7]=data1[i,7];
	if(data1[i,2]=="Monday") data2[i,2]=0;
	if(data1[i,2]=="Tuesday") data2[i,2]=1;
	if(data1[i,2]=="Wednesday") data2[i,2]=2;
	if(data1[i,2]=="Thursday") data2[i,2]=3;
	if(data1[i,2]=="Friday") data2[i,2]=4;
	if(data1[i,2]=="Saturday") data2[i,2]=5;
	if(data1[i,2]=="Sunday") data2[i,2]=6;
	data2[i,4]=as.numeric(strsplit(as.character(data1[i,4]),"_")[[1]][3]);
	data2[i,5]=as.numeric(strsplit(as.character(data1[i,5]),"_")[[1]][2]);
}

data2C <- data2;

data2 <- as.data.frame(data2);
colnames(data2) <- c("week","day","hour","flow","file","size","btime");

#------------------------------------------------------------------


data3=matrix(nrow=length,ncol=5);
for(i in 1:length) {
	data3[i,1]=(data2[i,1]-1)*7*24+data2[i,2]*24+data2[i,3];
	data3[i,2]=data2[i,4];
	data3[i,3]=data2[i,5];
	data3[i,4]=data2[i,6];
	data3[i,5]=data2[i,7];
}


#------------------------------------------------------------------


data4=data3[order(data3[,1]),];


#------------------------------------------------------------------


workflow=list(subset(data4,data4[,2]==0),
              subset(data4,data4[,2]==1),
              subset(data4,data4[,2]==2),
              subset(data4,data4[,2]==3),
              subset(data4,data4[,2]==4));


workflowa=list(subset(data2C,data2C[,4]==0),
              subset(data2C,data2C[,4]==1),
              subset(data2C,data2C[,4]==2),
              subset(data2C,data2C[,4]==3),
              subset(data2C,data2C[,4]==4));

workflowb=list(subset(data2,data2[,4]==0),
              subset(data2,data2[,4]==1),
              subset(data2,data2[,4]==2),
              subset(data2,data2[,4]==3),
              subset(data2,data2[,4]==4));

#------------------------------------------------------------------


workflowSumModel=matrix(nrow=timeLength,ncol=2);
workflowSum=list(workflowSumModel,
                 workflowSumModel,
                 workflowSumModel,
                 workflowSumModel,
                 workflowSumModel);
for(j in 1:5) {
  index=1;
  for(i in 1:timeLength) {
    tempSum=0;
    workflowSum[[j]][i,1]=i*4-3;
    while(index<=length(workflow[[j]][,1]) && workflow[[j]][index,1]==i*4-3) {
      tempSum=tempSum+workflow[[j]][index,4];
      index=index+1;
    }
    workflowSum[[j]][i,2]=tempSum;
  }
}


#------------------------------------------------------------------


totalflowSum=workflowSum[[1]]
for(i in 2:5) {
  totalflowSum[,2]=totalflowSum[,2]+workflowSum[[i]][,2];
}


#------------------------------------------------------------------


