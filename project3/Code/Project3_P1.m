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


% Save Original Data Values '.mat' File
save('R_raw.mat','R_raw');

% Creating R which missing some values
R=R_raw;
R(R==0) = NaN;

% LSE Values Matrix by each 'k' Values
P1_LSE=[10,0;50,0;100,0];


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
    
    
    % Weighted Least Square Error Collaborative Filtering
    option = struct([]);
    [A,Y,numIter,tElapsed,finalResidual]=wnmfrule(R,k,option)

    % Estimated R
    R_estimate = A*Y;

    % Total Least Squared Error
    LSE_Total = sum(sum(W.*(R_raw-R_estimate).^2));
    P1_LSE(i,2)=LSE_Total;
    
    % Creating Different Dataset by 'k' values and Save '.mat' File
    v = genvarname(['R_estimate_P1_k' num2str(k)],who);
    eval([v  '=R_estimate;']);
    save([v '.mat'],v);
end

% Save LSE Values '.mat' File
save('P1_LSE.mat','P1_LSE');


% 25, 57