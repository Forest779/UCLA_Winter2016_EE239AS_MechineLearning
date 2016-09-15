
from __future__ import print_function
import os
import csv,sys,json
import itertools
import collections, datetime, time
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from sklearn import svm
import pickle

global WINDOW
global SHIFT
global NUM_RAW_FTR

WINDOW = datetime.timedelta(hours=1)    # window length (1 hour)
SHIFT  = datetime.timedelta(hours=1)    # window shift (1 hour) : smaller shift will give higher time resolution
NUM_RAW_FTR = 3                         # the number of raw features

first_time_period_bin = datetime.datetime(2015, 2, 1, 8)
# first_time_period_timestamp = int(time.mktime(first_time_period_bin.timetuple()))
second_time_period_bin = datetime.datetime(2015, 2, 1, 20)
# second_time_period_timestamp = int(time.mktime(second_time_period_bin.timetuple()))


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



            
def get_more_features(time_info, raw_ftr, X, y):
    
    num_tweet = []
    for j in range(0,len(raw_ftr)):
        num_tweet.append(raw_ftr[j][0])
    
    delta1 = [0]*(len(num_tweet))
    delta2 = [0]*len(delta1)
  
    get_delta(num_tweet,delta1,2) 
    # get_delta(num_tweet,delta2,2)
    get_delta(delta1,delta2,2)
    
    for j in range(0,len(raw_ftr)):
        raw_ftr[j].append(delta1[j])                # feature4 : 1st-order time-derivative
        raw_ftr[j].append(delta2[j])                # feature5 : 2nd-order time-derivative
        
    interval = int(np.ceil(float(datetime.timedelta(hours=1).seconds)/SHIFT.seconds))

    for j in range(0, (len(raw_ftr)-interval)):
        X.append(raw_ftr[j])
        y.append(num_tweet[j+interval])


def get_raw_features(path, time_info,raw_ftr,period): 
    print('Get Features : ',path)
    flag = 0;
    with open(path,"r") as fin:
        for line in fin:
            tweet = json.loads(line)
            
            current_time = datetime.datetime.fromtimestamp(tweet['firstpost_date'])        
            
            flag = 0
            
            if period == 1:
                if current_time < first_time_period_bin:
                    flag = 1
            elif period == 2:
                if (current_time >= first_time_period_bin) and (current_time <= second_time_period_bin):
                    flag = 1
            elif period == 3:
                if current_time > second_time_period_bin:
                    flag = 1
            elif period == 4:
                flag = 1
                    
                    
            
            if flag == 1:                   
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
                      
    fin.close() 




def regression_model(X,y):    
    X = np.array(X)
    y = np.transpose(y)
    
    X = sm.add_constant(X)
    
    # linear regression
    model = sm.OLS(y,X)
    results = model.fit()
    coeff = results.params # coefficients, including constant
    
    coeff_list_general.append(coeff)


def predict_by_model(period):
    error = []

    for i in range(0,len(X)):
        predict_value = coeff_list_general[period-1][1]*X[i][0] + coeff_list_general[period-1][2]*X[i][1] + coeff_list_general[period-1][3]*X[i][2] + coeff_list_general[period-1][4]*X[i][3] + coeff_list_general[period-1][5]*X[i][4] + coeff_list_general[period-1][0]
        if i+1 < len(X):
            error.append(abs(predict_value - X[i+1][0]))
        
    
    # Select the minimum Error model and get the Predict Value
    # choose model -> hashtag
    predict.append(predict_value)
    avg_error_list.append(sum(error)/len(X))




# ================================ start ===================================

X = []; y=[];
time_info=[]; raw_ftr=[];
coeff_list_general = [];


for i in range(1,4):
    X = []; y=[];
    time_info=[]; raw_ftr=[];
    
    #get_raw_features('./tweet_data/tweets_#whatever.txt', time_info, raw_ftr)
    print('Period : ',i,' Start')
    # ----- read raw features from files :
    #  running one-by-one files, time bins and (raw) features will be added automatically

    tweet_data_path = './tweet_data/'
    get_raw_features(tweet_data_path+'tweets_#gopatriots.txt', time_info, raw_ftr,i)
    get_raw_features(tweet_data_path+'tweets_#gohawks.txt', time_info, raw_ftr,i)
    get_raw_features(tweet_data_path+'tweets_#patriots.txt', time_info, raw_ftr,i)
    get_raw_features(tweet_data_path+'tweets_#superbowl.txt', time_info, raw_ftr,i)
    get_raw_features(tweet_data_path+'tweets_#nfl.txt', time_info, raw_ftr,i)
    get_raw_features(tweet_data_path+'tweets_#sb49.txt', time_info, raw_ftr,i)
    
    # ---- finalize feature array :
    #  add some features derived from the raw features
    #  and finalize the feature array X and the target y
    get_more_features(time_info, raw_ftr, X, y)
    
    regression_model(X,y)
    
    print('Period : ',i,' Finish')

"""
# Save Coefficients by 3 periods
path = "D:\Users\1234\Desktop\special code\tweet_data\"
f = open(path+'coeff_list_general.pckl','w')
pickle.dump(coeff_list_general,f)
f.close()

path = "D:/Users/1234/Desktop/special_code/tweet_data/"

f = open(path+'coeff_list_general.pckl')
coeff_list_general = pickle.load(f)
f.close()
"""

# ---------- Prediction of Test Tweet Files
# You should set the path data file located
tweet_test_path = './test_data/'

predict = []
avg_error_list = []
testfile_array = []

for file in os.listdir(tweet_test_path):
    if file.endswith(".txt"):
        X = []; y=[];
        time_info=[]; raw_ftr=[];
        
        print('Start Process : ',file)
        file_path = tweet_test_path+file
        print(file_path)
        get_raw_features(file_path, time_info, raw_ftr,4)
        get_more_features(time_info, raw_ftr, X, y)
        predict_by_model(int(str(file)[-5]))
        testfile_array.append(file.replace(".txt", ""))
        print('Finish Process : ',file)

print('Predict : ',predict)
print('Error : ',avg_error_list)