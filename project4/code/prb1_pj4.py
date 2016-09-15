import csv,sys, json
import collections, datetime, time
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from matplotlib.backends.backend_pdf import PdfPages


global WINDOW
global SHIFT
#global NUM_RAW_FTR

WINDOW = datetime.timedelta(hours=1)    # window length (1 hour)
SHIFT  = datetime.timedelta(hours=0.5)    # window shift (1 hour) : smaller shift will give higher time resolution
#NUM_RAW_FTR = 4                         # the number of raw features






def get_num_tweet_per_hour(path, time_info,number_tweet):
    

 
    
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
                    number_tweet.insert(0,0)
                else:
                    
                    while current_time < (time_info[0]+WINDOW-SHIFT):
                        time_info.insert(0, time_info[0]-SHIFT)
                        number_tweet.insert(0,0)


            
            elif current_time >= (time_info[len(time_info)-1]+WINDOW-SHIFT):
                
                while current_time >= (time_info[len(time_info)-1]+WINDOW-SHIFT):
                    last_time_info = time_info[len(time_info)-1]
                    time_info.append(last_time_info+SHIFT)
                    number_tweet.append(0)

                    
                

            # -------- put data into feature array --------------------
            #number_retweet  = tweet['metrics']['citations']['total']                
            #number_follower = tweet['author']['followers']
            
            # find a right place to put data in
            for j in range(0, len(time_info)):
                if time_info[j]<=current_time  and current_time<(time_info[j]+WINDOW):
                    
                    number_tweet[j] += 1

                        
    fin.close() 
            
            



def plot_num_tweet_per_hour(time_info, number_tweet,hashTag):
    pp = PdfPages('p1_plots_'+hashTag+'.pdf')
    
    # ------------ plot for whole time range -------------------------
    N=3 # show xlabel at every N day
    
    
    time_tick_N_day = []
    time_label_N_day = []
    for j in range(0,len(time_info)):
        current_time = time_info[j]
        if (j*SHIFT).days%N ==0 and current_time.hour == 0:
        #if (time_info[0].hour+24*((j*SHIFT).day))%(24*N) == 0 :
            #current_day = current_time.day
            
            time_tick_N_day.append(j)
            time_label_N_day.append(current_time.strftime("%m/%d"))

    fig1 = plt.figure()
    fig1.subplots_adjust(bottom=0.2)
    ax1 = fig1.add_subplot(111)
    hist1 = ax1.bar(range(0,len(time_info)), number_tweet)
    ax1.set_xticks(time_tick_N_day)          
    ax1.set_xticklabels(time_label_N_day, rotation=45)    
    
    plt.xlabel('time (date)')
    plt.ylabel('the number of tweets')
    
    
    # plt.show() 
    #plt.savefig(pp, format='pdf')
    
    
    # ------------ plot for the superbowl day -------------------------
                
    
    min_date = datetime.datetime(2015,2,1, 8)    
    
    max_date = datetime.datetime(2015,2,1,20)    
    
    
    zoom_time_info=[]
    zoom_frequency=[]
    zoom_tick=[];zoom_label=[]
    for j in range(0,len(time_info)):
        current_time = time_info[j]
        #current_hour = start_time+datetime.timedelta(hours=x)
        
        if (min_date<=current_time) and (current_time<=max_date):
            zoom_time_info.append(j)
            zoom_frequency.append(number_tweet[j])
            
            if current_time.minute == 0:
                zoom_tick.append(j)
                zoom_label.append(current_time.strftime("%I:%M%p"))    
    
    
    
    
    fig2 = plt.figure()
    fig2.subplots_adjust(bottom=0.2)
    ax2 = fig2.add_subplot(111)
    hist2 = ax2.bar(zoom_time_info, zoom_frequency)
    ax2.set_xticks(zoom_tick)      
    ax2.set_xticklabels(zoom_label, rotation=45)   
    
    plt.xlabel('time')
    plt.ylabel('the number of tweets')
    
    # plt.show() 
    
    plt.savefig(pp, format='pdf')
    pp.close()
# ================================ start ===================================


#time_info=[]; number_tweet=[];
#get_num_tweet_per_hour('./tweet_data/tweets_#nfl.txt', time_info,number_tweet)
#plot_num_tweet_per_hour(time_info, number_tweet, '#nfl')

time_info=[]; number_tweet=[];
get_num_tweet_per_hour('../tweet_data/tweets_#superbowl.txt', time_info,number_tweet)
plot_num_tweet_per_hour(time_info, number_tweet, '#superbowl')

#get_raw_features('./tweet_data/tweets_#whatever.txt', time_info, raw_ftr)


# ----- read raw features from files :
#  running one-by-one files, time bins and (raw) features will be added automatically
#get_raw_features('./tweet_data/tweets_#gopatriots.txt', time_info, raw_ftr)
#get_raw_features('./tweet_data/tweets_#patriots.txt', time_info, raw_ftr)

#get_raw_features('./tweet_data/tweets_#gohawks.txt', time_info, raw_ftr)
#get_raw_features('./tweet_data/tweets_#sb49.txt', time_info, raw_ftr)

# ---- finalize feature array :
#  add some features derived from the raw features
#  and finalize the feature array X and the target y


