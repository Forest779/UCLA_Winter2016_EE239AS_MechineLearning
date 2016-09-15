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


known_indices = find(R_raw ~= 0);
W(known_indices) = R_raw(known_indices);

% Creating R which missing some values
R=ceil(R_raw./5);
R_original = R;
R(R==0) = NaN;

% LSE Values Matrix by each 'k' Values
%P4_LSE=[10,0;50,0;100,0];
P4_LSE_1=[10,0;50,0;100,0];

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
   [A,Y,numIter,tElapsed,finalResidual]=wnmfruleP4(R,k,option,W);
    %[A,Y,numIter,tElapsed,finalResidual]=wnmfrule_als(R,k,0.01,option,W);

    % Estimated R
    R_estimate = (A*Y);

    
    % Total Least Squared Error
    LSE_Total = sum(sum((W.*(ceil(R_raw./5)-R_estimate)).^2));
    P4_LSE_1(i,2)=LSE_Total;
    
    % Creating Different Dataset by 'k' values and Save '.mat' File
    v = genvarname(['R_estimate_P4_k' num2str(k)],who);
    eval([v  '=R_estimate;']);
    save([v '.mat'],v);
end

%Creating Different Dataset by 'k' values and Save '.mat' File
save('P4_LSE.mat','P4_LSE');