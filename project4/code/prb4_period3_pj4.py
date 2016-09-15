from sklearn.cross_validation import KFold
import csv,sys, json
import collections, datetime, time
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

global WINDOW
global SHIFT
global NUM_RAW_FTR

WINDOW = datetime.timedelta(hours=1)    # window length (1 hour)
SHIFT  = datetime.timedelta(hours=1)    # window shift (1 hour) : smaller shift will give higher time resolution
NUM_RAW_FTR = 3                         # the number of raw features

# timestamp value for spliting periods
first_time_period_bin = datetime.datetime(2015, 2, 1, 8)
second_time_period_bin = datetime.datetime(2015, 2, 1, 20)

# function to compute delta feature value
def get_delta(x, d, DELTA_WINDOW):
    for t in range(len(x)):       
        if t<DELTA_WINDOW:
            d[t] = x[t-1]-x[t]
        elif t>= len(x)-DELTA_WINDOW:
            d[t] = x[t] - x[t-1]
        else:
            d[t] = 0; den = 0
            for m in range(1,DELTA_WINDOW+1):
                d[t] += m*((x[t+m])-x[t-m])
                den += 2*(m**2)
            d[t] = d[t]/den

#  function to compute a list of raw features from all hashtags' tweet data
def get_raw_features(path, time_info,raw_ftr): 
    with open(path,"r") as fin:
        for line in fin:
            tweet = json.loads(line)
            
            current_time = datetime.datetime.fromtimestamp(tweet['firstpost_date'])        
            
             # if current_time < first_time_period_bin: # period 1
            # if (current_time >= first_time_period_bin) and (current_time <= second_time_period_bin): # period 2
            if current_time > second_time_period_bin: # period 3   
                # -------- create time bins --------------------
                if (not time_info) or (current_time<=time_info[0]):
                    # if time_info is empty or new data is from the previous time
                    start_time = current_time
                    first_min_time = datetime.datetime(start_time.year, start_time.month, start_time.day, start_time.hour)
                    
                    if not time_info:
                        time_info.insert(0,first_min_time)
                        raw_ftr.insert(0,[float(0)]*NUM_RAW_FTR)
                    else:
                        while current_time < (time_info[0]+WINDOW-SHIFT):
                            time_info.insert(0, time_info[0]-SHIFT)
                            raw_ftr.insert(0,[float(0)]*NUM_RAW_FTR)

                elif current_time >= (time_info[len(time_info)-1]+WINDOW-SHIFT):               
                    while current_time >= (time_info[len(time_info)-1]+WINDOW-SHIFT):
                        last_time_info = time_info[len(time_info)-1]
                        time_info.append(last_time_info+SHIFT)
                        raw_ftr.append([float(0)]*NUM_RAW_FTR)

                # -------- put data into feature array --------------------
                num_retweet  = tweet['metrics']['citations']['total']                
                num_follower = tweet['tweet']['user']['followers_count']
                num_mention = len(tweet['tweet']['entities']['user_mentions'])
                
                # find a right place to put data in
                for j in range(0, len(time_info)):
                    if time_info[j]<=current_time  and current_time<(time_info[j]+WINDOW):
                        raw_ftr[j][0] += 1                    # feature1 : number of tweets    
                        raw_ftr[j][1] += num_follower         # feature2 : sum of the numbers of followers
                        raw_ftr[j][2] += num_mention          # feature3 : number of mention
                
    print "Feature Generation from raw data in #%s is done" % path.split("#")[1].replace(".txt", "")
    fin.close() 
            
# function to calculate additional features from raw features
def get_more_features(time_info, raw_ftr, X, y):
    
    num_tweet = []
    for j in range(0,len(raw_ftr)):
        num_tweet.append(raw_ftr[j][0])
    
    delta1 = [0]*(len(num_tweet))
    delta2 = [0]*len(delta1)
  
    get_delta(num_tweet,delta1,2) 
    get_delta(delta1,delta2,2)
    
    for j in range(0,len(raw_ftr)):
        raw_ftr[j].append(delta1[j])                # feature4 : 1st-order time-derivative
        raw_ftr[j].append(delta2[j])                # feature5 : 2nd-order time-derivative
        
    interval = int(np.ceil(float(datetime.timedelta(hours=1).seconds)/SHIFT.seconds))

    for j in range(0, (len(raw_ftr)-interval)):
        X.append(raw_ftr[j])
        y.append(num_tweet[j+interval])

    print "Addition Feature Generation from existing features is done"

# function to do cross-validation and write output file 
def cross_validation(X, y):

    fout = open('p4_output_period3.txt', 'w')
    X = np.array(X)

    cv = KFold(len(X), 10)

    count = 0
    error_list_each_test = []
    for train, test in cv:
        count += 1
        print 'Test: ',count
        fout.write('Test: '+str(count) + '\n')
        train_x1 = []; train_x2 = []; train_x3 = []; train_x4 = []; train_x5 = []
        for i in train:
            train_x1.append(X[i][0]); train_x2.append(X[i][1]); train_x3.append(X[i][2]);
            train_x4.append(X[i][3]); train_x5.append(X[i][4])

        temp_X=np.column_stack((train_x1[0:len(train_x1)-1], train_x2[0:len(train_x2)-1], train_x3[0:len(train_x3)-1],
         train_x4[0:len(train_x4)-1], train_x5[0:len(train_x5)-1])) # first 4
        
        # create target vector
        num_tweets_next_hour = train_x1[1:len(train_x1)]
        y=np.transpose(num_tweets_next_hour)
        temp_X = sm.add_constant(temp_X)
        
        # linear regression
        model = sm.OLS(y,temp_X)
        results = model.fit()
        # print(results.summary())  
        fout.write(str(results.summary())+'\n\n')

        coeffs = results.params
        
        # print coeffs
        # print len(feature_set), len(test)
        error_list_each_element = []
        for j in test:
            # print "test element: ", j
            predict_value = coeffs[1]*X[j][0] + coeffs[2]*X[j][1] + coeffs[3]*X[j][2]
            + coeffs[4]*X[j][3] + coeffs[5]*X[j][4] + coeffs[0]
            
            error_each_element = abs(predict_value - X[j][0])
            error_list_each_element.append(error_each_element)
            
            # print "original value: ", X[j][0], j
            # print 'predicted value: ', predict_value
            # print "error by individual element: ", error_each_element

        average_error_each_iteration = np.mean(error_list_each_element)
        print "Average error in each test: ", average_error_each_iteration
        error_list_each_test.append(average_error_each_iteration)

    for i in range(0,len(error_list_each_test)):
        fout.write("Average error in each test %d: %s \n" % (i , str(error_list_each_test[i])))
    print 'Average error among 10 tests: ', np.mean(error_list_each_test)
    fout.write('Average error among 10 tests: ' + str(np.mean(error_list_each_test)))
    fout.close()

# ================================ start ===================================

X = []; y=[];
time_info=[]; raw_ftr=[];
# ----- read raw features from files :
#  running one-by-one files, time_info and (raw) features will be added automatically
get_raw_features('./tweet_data/tweets_#gopatriots.txt', time_info, raw_ftr)
get_raw_features('./tweet_data/tweets_#gohawks.txt', time_info, raw_ftr)
get_raw_features('./tweet_data/tweets_#patriots.txt', time_info, raw_ftr)
get_raw_features('./tweet_data/tweets_#superbowl.txt', time_info, raw_ftr)
get_raw_features('./tweet_data/tweets_#nfl.txt', time_info, raw_ftr)
get_raw_features('./tweet_data/tweets_#sb49.txt', time_info, raw_ftr)

# ---- finalize feature array :
#  add some features derived from the raw features
#  and finalize the feature array X and the target y
get_more_features(time_info, raw_ftr, X, y)

# -------- do cross validation------------
cross_validation(X, y)