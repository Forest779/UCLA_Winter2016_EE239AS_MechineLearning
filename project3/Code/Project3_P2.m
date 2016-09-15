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


% Part2
% ABS_ERR Each Row : Different 'k', Each Column : Iteration Number
% End of Column : Average Error
P2_ABS_ERR = [10,0,0,0,0,0,0,0,0,0,0,0;50,0,0,0,0,0,0,0,0,0,0,0;100,0,0,0,0,0,0,0,0,0,0,0];


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
        R = R_raw;
        R(test_indices) = 0;
        R(R==0) = NaN;

        % Weighted Least Square Error Collaborative Filtering
        option = struct([]);
        [A,Y,numIter,tElapsed,finalResidual]=wnmfrule(R,k,option);

        % Estimated R
        R_estimate = A*Y;

        % Extract Testing Data From Original and Estimate
        %R_raw_TestIndices = R_raw(test_indices);
        %R_estimate_TestIndices = R_estimate(test_indices);
        R_raw_TestIndices = R_raw(test_indices);
        R_estimate_TestIndices = R_estimate(test_indices);
        
        % Absolute Error
        P2_ABS_ERR(i,j+1) = sum(sqrt((R_raw_TestIndices-R_estimate_TestIndices).^2))/(N/10);
    end
    
    % Average Absolute Error
    P2_ABS_ERR(i,12) = mean(P2_ABS_ERR(i,2:11));

end

% Save Absolute Error Values '.mat' File
save('P2_ABS_ERR.mat','P2_ABS_ERR');


% Save all Workspace
save('P2_Workspace.mat');

% 