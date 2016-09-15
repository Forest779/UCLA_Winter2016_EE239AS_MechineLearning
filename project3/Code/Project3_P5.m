% Add Path for wnmfrule function
mfilepath=fileparts(which(mfilename));
addpath(fullfile(mfilepath,'./nmfv1_4'));
%addpath('.\nmfv1_4');

clear all;

% Loading Data File
R_data = importdata('u.data');

%Creating hit_rate and false_alarm_rate Matrix
hit_rate = zeros(3,10,20);
false_alarm_rate = zeros(3,10,20);
precision = zeros(3,10,20);
hit_rate_ave = zeros(3,20);
false_alarm_rate_ave = zeros(3,20);
precision_ave = zeros(3,20);


% Creating Matrix R & W
R_raw = zeros(943,1682);
W = zeros(943,1682);
for n=1:size(R_data)
	R_raw(R_data(n,1),R_data(n,2)) = R_data(n,3);
end
W = ceil(R_raw./5);
temp = R_raw;
R_raw = W;
W = temp;
R_raw_W = R_raw.*W;

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
        R_estimate_W = R_estimate.*W;

        

        %find the threshold for top L
        for L = 1:20
            raw_temp = zeros(943,1682);
            estimate_temp = zeros(943,1682);
            for row = 1:943
                temp = fliplr(sort(R_estimate_W(row,:)));
                topshold_estimate = temp(L);
                temp = fliplr(sort(R_raw_W(row,:)));
                topshold_raw = temp(L);

                %only remain the top L movies for each row 

                for col = 1:1682
                    if R_raw_W(row,col) < topshold_raw
                        raw_temp(row,col) = 0;
                    else
                        raw_temp(row,col) = 1;
                    end

                    if R_estimate_W(row,col) < topshold_estimate
                        estimate_temp(row,col) = 0;
                    else
                        estimate_temp(row,col) = 1;
                    end
                end
            end

            % Extract Testing Data From Original and Estimate
            R_raw_TestIndices = raw_temp(test_indices);
            R_estimate_TestIndices = estimate_temp(test_indices);
            R_result = R_estimate_TestIndices - R_raw_TestIndices;

            % Calculate the hit rate and the false-alarm rate
            t_like = 0;
            t_not_like = 0;
            s_like = 0;
            s_not_like = 0;
            l_to_n_case = 0;
            n_to_l_case = 0;
            r_case = 0;
            for i_test = 1:(N/10)
                if R_raw_TestIndices(i_test) == 0
                    t_not_like = t_not_like + 1;
                else
                    t_like = t_like + 1;
                end
                if R_estimate_TestIndices(i_test) == 0
                    s_not_like = s_not_like + 1;
                else
                    s_like = s_like + 1;
                end
                if R_result(i_test) == 0
                    r_case = r_case + 1;
                elseif R_result(i_test) == 1
                    n_to_l_case = n_to_l_case + 1;
                else
                    l_to_n_case = l_to_n_case + 1;
                end
            end

            hit_rate(i,j,L) = (t_like - l_to_n_case)/(t_like);
            false_alarm_rate(i,j,L) = (n_to_l_case)/(t_not_like);
            precision(i,j,L) = (s_like - n_to_l_case)/s_like;

        end
    end

    for L = 1:20
        hit_rate_ave(i,L) = mean(hit_rate(i,:,L));
        false_alarm_rate_ave(i,L) = mean(false_alarm_rate(i,:,L));
        precision_ave(i,L) = mean(precision(i,:,L));
    end
end

figure
title('plot ROC curve')
subplot(3,1,1)
plot(hit_rate_ave(1,:),false_alarm_rate_ave(1,:));
ylabel('false_alarm_rate','fontsize', 10);
xlabel('hit_rate','fontsize', 10);
grid on
subplot(3,1,2)
plot(hit_rate_ave(2,:),false_alarm_rate_ave(2,:));
ylabel('false_alarm_rate','fontsize', 10);
xlabel('hit_rate','fontsize', 10);
grid on
subplot(3,1,3)
plot(hit_rate_ave(3,:),false_alarm_rate_ave(3,:));
ylabel('false_alarm_rate','fontsize', 10);
xlabel('hit_rate','fontsize', 10);
grid on

title(subplot(3,1,1),'plot ROC curve k=10')
title(subplot(3,1,2),'plot ROC curve k=50')
title(subplot(3,1,3),'plot ROC curve k=100')


