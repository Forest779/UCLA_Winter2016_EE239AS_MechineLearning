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
NUM_RAW_FTR = 4                         # the number of raw features

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



def get_raw_features(path, time_info,raw_ftr):
    
#    WINDOW = datetime.timedelta(hours=1)    # window length (1 hour)
#    SHIFT  = datetime.timedelta(hours=1)    # window shift (1 hour) : smaller shift will give higher time resolution
#    NUM_RAW_FTR = 4                         # the number of raw features
# 
    
    with open(path,"r") as fin:
        for line in fin:
            tweet = json.loads(line)
            
            current_time = datetime.datetime.fromtimestamp(tweet['firstpost_date'])
            
            
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
            num_follower = tweet['author']['followers']
            
            # find a right place to put data in
            for j in range(0, len(time_info)):
                if time_info[j]<=current_time  and current_time<(time_info[j]+WINDOW):
                    
                    
                    raw_ftr[j][0] += 1                    # feature1 : number of tweets    
                    raw_ftr[j][1] += num_retweet          # feature2 : total number of retweets
                    raw_ftr[j][2] += num_follower         # feature3 : sum of the numbers of followers
                    raw_ftr[j][3] = max(raw_ftr[j][3], num_follower)   # feature4 : max number of followers

                    
                    
                        
    fin.close() 
            
            
def get_more_features(time_info, raw_ftr, X, y):
    
    number_tweet = []
    for j in range(0,len(raw_ftr)):
        number_tweet.append(raw_ftr[j][0])
    

    delta1 = [0]*len(number_tweet)
    delta2 = [0]*len(delta1)
    
    get_delta(number_tweet,delta1,2) 
    get_delta(number_tweet,delta2,2)
    
    
    for j in range(0,len(raw_ftr)):
        timeOfDay = time_info[j].hour+time_info[j].minute/float(60)+time_info[j].second/float(3600)
        
        raw_ftr[j].append(timeOfDay)                # feature5 : time of the day
        #raw_ftr[j].append(delta1[j])                # feature6 : 1st-order time-derivative
        #raw_ftr[j].append(delta2[j])                # feature7 : 2nd-order time-derivative
        
    
    interval = int(np.ceil(float(datetime.timedelta(hours=1).seconds)/SHIFT.seconds))
    for j in range(0, (len(raw_ftr)-interval)):
        X.append(raw_ftr[j])
        y.append(number_tweet[j+interval])


def ordinary_lin_regression(X,y):
    
    X = np.array(X)
    y = np.transpose(y)
    
    X = sm.add_constant(X)
    
    # linear regression
    model = sm.OLS(y,X)
    results = model.fit()
    print(results.summary())  
    


# ================================ start ===================================

X = []; y=[];
time_info=[]; raw_ftr=[];


# ----- read raw features from files :
#  running one-by-one files, time info and (raw) features will be added automatically
#get_raw_features('./tweet_data/tweets_#gopatriots.txt', time_info, raw_ftr)
#get_raw_features('./tweet_data/tweets_#patriots.txt', time_info, raw_ftr)
#get_raw_features('./tweet_data/tweets_#superbowl.txt', time_info, raw_ftr)
#get_raw_features('./tweet_data/tweets_#nfl.txt', time_info, raw_ftr)
#get_raw_features('./tweet_data/tweets_#gohawks.txt', time_info, raw_ftr)
get_raw_features('../tweet_data/tweets_#sb49.txt', time_info, raw_ftr)

# ---- finalize feature array :
#  add some features derived from the raw features
#  and finalize the feature array X and the target y
get_more_features(time_info, raw_ftr, X, y)

# -------- model fit------------
ordinary_lin_regression(X,y) 
