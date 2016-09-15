% Add Path for wnmfrule function
mfilepath=fileparts(which(mfilename));
addpath(fullfile(mfilepath,'./nmfv1_4'));
%addpath('.\nmfv1_4');

clear all;

% Loading Data File
R_data = importdata('u.data');

% Creating Matrix R & W
R_raw = zeros(943,1682);
W = zeros(943,1682);
for n=1:size(R_data)
	R_raw(R_data(n,1),R_data(n,2)) = R_data(n,3);
end
W = ceil(R_raw./5);

% Preparing Test indices
known_indices = find(R_raw ~= 0);
N = length(known_indices);
prm = randperm(N);


% Method By Part3
% ABS_ERR Each Row : Different 'k', Each Column : Iteration Number
% End of Column : Average Error
P3_ABS_ERR = [10,0,0,0,0,0,0,0,0,0,0,0;50,0,0,0,0,0,0,0,0,0,0,0;100,0,0,0,0,0,0,0,0,0,0,0];

% Repeat 3 by different 'k' Values
for i=1:3
    
    % 'k' Value define
    switch i
        case 1
            k = 10;
        case 2
            k = 50;
        case 3
            k = 100;
    end
    
    
    for j=1:10
        % Iterating 10 times with Random Testing
        test_indices = known_indices(prm((j-1)*10000+1:j*10000));

        % Creating R which missing some values
        R=R_raw;
        R(test_indices)=0;
        R(R==0) = NaN;

        % Weighted Least Square Error Collaborative Filtering
        option = struct([]);
        [A,Y,numIter,tElapsed,finalResidual]=wnmfrule(R,k,option);

        % Estimated R
        R_estimate = (A*Y);

        % Extract Testing Data From Original and Estimate
        R_raw_TestIndices = R_raw(test_indices);
        R_estimate_TestIndices = R_estimate(test_indices);
        

        %threshold
        index = 0;
        for threshold=0:0.1:10
            index = index + 1;
            test_ratings = R_raw_TestIndices;
            pred_ratings = R_estimate_TestIndices;
            P3_PRE_REC(1,j,index,i) = length(find(test_ratings>3 & pred_ratings>threshold))/length(find(pred_ratings>threshold));
            P3_PRE_REC(2,j,index,i) = length(find(test_ratings>3 & pred_ratings>threshold))/length(find(test_ratings>3));
        end
        
        % Absolute Error
        P3_ABS_ERR(i,j+1) = sum(sqrt((R_raw_TestIndices-R_estimate_TestIndices).^2))/(N/10);
    end
    
    % Average Absolute Error
    P3_ABS_ERR(i,12) = mean(P3_ABS_ERR(i,2:11));

end

for k=1:3
    index = 0;
    for threshold=0:0.1:10
        index = index + 1;
        P3_MEAN_PRE_REC(1,index,k) = mean(P3_PRE_REC(1,:,index,k));
        P3_MEAN_PRE_REC(2,index,k) = mean(P3_PRE_REC(2,:,index,k));
    end
end

figure
subplot(3,1,1)
%plot(1:4,P3_MEAN_PRE_REC(2,:,1),'-b',1:4,P3_MEAN_PRE_REC(1,:,1),'--r');
plot(P3_MEAN_PRE_REC(2,:,1),P3_MEAN_PRE_REC(1,:,1));
ylabel('Precision');
xlabel('Recall');
grid on
subplot(3,1,2)
%plot(1:4,P3_MEAN_PRE_REC(1,:,2),'-b',1:4,P3_MEAN_PRE_REC(2,:,2),'--r');
plot(P3_MEAN_PRE_REC(2,:,2),P3_MEAN_PRE_REC(1,:,2));
ylabel('Precision');
xlabel('Recall');
grid on
subplot(3,1,3)
%plot(1:4,P3_MEAN_PRE_REC(1,:,3),'-b',1:4,P3_MEAN_PRE_REC(2,:,3),'--r');
plot(P3_MEAN_PRE_REC(2,:,3),P3_MEAN_PRE_REC(1,:,3));
ylabel('Precision');
xlabel('Recall');
grid on

title(subplot(3,1,1),'plot ROC curve k=10')
title(subplot(3,1,2),'plot ROC curve k=50')
title(subplot(3,1,3),'plot ROC curve k=100')

% Save Absolute Error Values '.mat' File
save('P3_ABS_ERR.mat','P3_ABS_ERR');
save('P3_MEAN_PRE_REC.mat','P3_MEAN_PRE_REC');

% Save all Workspace
save('Project3_P3_Workspace.mat');

%calculate under area
for k_loop=1:3
sum_area=0;
cal_area=0;
for are_loop=1:30
cal_area=P3_MEAN_PRE_REC(1,are_loop,k_loop)*(P3_MEAN_PRE_REC(2,are_loop,k_loop)-P3_MEAN_PRE_REC(2,are_loop+1,k_loop))+(P3_MEAN_PRE_REC(1,are_loop+1,k_loop)-P3_MEAN_PRE_REC(1,are_loop,k_loop))*(P3_MEAN_PRE_REC(2,are_loop,k_loop)-P3_MEAN_PRE_REC(2,are_loop+1,k_loop))/2;
sum_area=cal_area+sum_area;
end
P3_ROC_area(1,k_loop)=sum_area;
end

for k = 1:3
area(k) = trapz(P3_MEAN_PRE_REC(2,:,k),P3_MEAN_PRE_REC(1,:,k));
end

