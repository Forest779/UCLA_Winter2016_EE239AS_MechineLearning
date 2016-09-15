import csv,sys,json
import itertools
import collections, datetime, time
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from sklearn import svm

month_dict = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7,'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

x1 = [0] # feature1 : number of tweet    
x2 = [0] # feature2 : total number of retweets
x3 = [0] # feature3 : sum of the numbers of followers
x4 = [0] # feature4 : max number of followers
x5 = [0] # feature5 : time of the day
x6 = [0] # feature6 : duckha made
x7 = [0] # feature7 : duckha made
x8 = [0] # feature8 : number of mention
x9 = [0] # feature9 : url ratio                                     remove
temp_x9 = [0] # temp_list to compute feature9                       remove
x10 = [0] # feature10 : passivity (total)
x11 = [0] # feature10 : passivity (average)
x12 = [0] # feature10 : passivity (max)
x13 = [0] # feature11 : co-occurence times with other hashtags      remove
x14 = [0] # feature12 : case-sentitive hashtag count                remove
x15 = [0] # feature13 : special signals                             remove


# function to compute delta features
def get_delta(x, d, DELTA_WINDOW):
    for t in range(len(x)):    
        if t<DELTA_WINDOW:
            d[t] = x[t-1]-x[t]
        elif t>= len(x)-DELTA_WINDOW:
            d[t] = x[t] - x[t-1]
        else:
            d[t] = 0; den = 0
            for m in range(1,DELTA_WINDOW+1):
                d[t] += m*(x[t+m]-x[t-m])
                den += 2*(m**2)
            d[t] = d[t]/den
                

#  function to produce features from hashtag tweet data
def get_features(path):
    tot_count = 0; time_count = 0; tweet_count = 0
    with open(path, "r") as fin:
        for line in fin:
            tweet = json.loads(line)
            
            tot_count += 1
            current_date = tweet['firstpost_date']
            
            # start the time info with the first tweet 
            if tot_count==1:
                    start_time = datetime.datetime.fromtimestamp(current_date)
    
                    first_time_info = datetime.datetime(start_time.year, start_time.month, start_time.day, start_time.hour)
                    first_min_date = int(time.mktime(first_time_info.timetuple()))
                    current_min_date = first_min_date
                    
                    x5[time_count] = datetime.datetime.fromtimestamp(current_min_date).hour
            
            # add time info when current tweet is posted more than 1 hour later than current time
            elif current_min_date+3600<=current_date:
                while current_min_date+3600<=current_date:
                    x1.append(0); x2.append(0); x3.append(0); x4.append(0)
                    x5.append(0); x8.append(0); x9.append(0); temp_x9.append(0)
                    x10.append(0); x11.append(0); x12.append(0); x13.append(0)
                    x14.append(0); x15.append(0)

                    tweet_count = 0
                    time_count += 1
                    current_min_date += 3600
                    x5[time_count] = datetime.datetime.fromtimestamp(current_min_date).hour
        
            # add frequency only when the tweet is posted exactly between min and max of current time
            if current_min_date<=current_date & current_date<current_min_date+3600:
                num_retweet  = tweet['metrics']['citations']['total']                
                num_follower = tweet['tweet']['user']['followers_count']
                num_mention = len(tweet['tweet']['entities']['user_mentions'])
                tweet_text = tweet['tweet']['text']
                num_tweet_this_user = tweet['tweet']['user']['statuses_count']
                num_cooccur_hashtags = len(tweet['tweet']['entities']['hashtags'])
                list_hashtags = tweet['tweet']['entities']['hashtags']

                # extract date information about when current tweet is posted
                current_time = datetime.datetime.fromtimestamp(current_date)
                curent_time_info = datetime.datetime(current_time.year, current_time.month, current_time.day, current_time.hour)  
                current_min_date = int(time.mktime(curent_time_info.timetuple()))
                
                # extract date information about when this user created his/her account
                created_date = tweet['tweet']['user']['created_at']
                list_of_date = created_date.split(" ")
                year = int(list_of_date[5])
                month = month_dict[list_of_date[1]]
                day = int(list_of_date[2])
                hour = int(list_of_date[3].split(":")[0])

                #  compute timestamp value based on above info
                created_time_info = datetime.datetime(year, month, day, hour)
                created_time_date = int(time.mktime(created_time_info.timetuple()))
                number_of_days = (current_min_date - created_time_date) / (3600 * 24)
                passivity_each = round(float(number_of_days) / (1 + num_tweet_this_user), 3)

                # make a list of features based on computation
                tweet_count += 1
                x10[time_count] += passivity_each
                x11[time_count] = round(x10[time_count] / tweet_count, 3)
                x12[time_count] = max(x12[time_count], passivity_each)
                x1[time_count] += 1
                x2[time_count] += num_retweet
                x3[time_count] += num_follower
                x4[time_count] = max(x4[time_count], num_follower)
                x8[time_count] += num_mention
                x13[time_count] += num_cooccur_hashtags
                
                # make feature x9
                if "https://" in tweet_text or "http://" in tweet_text:
                    temp_x9[time_count] += 1
                x9[time_count] = round(temp_x9[time_count] / float(x1[time_count]), 3)

                # make feature x14
                target = path.split("#")[1].replace(".txt","")
                target_count = 0
                for hashtag in list_hashtags:
                    if hashtag['text'].lower() == target:
                        target_count += 1
                    if target_count > 1:
                        x14[time_count] += 1

                # make feature x15
                list_characters_in_tweet_text = [''.join(value) for key, value in itertools.groupby(tweet_text)]
                for elem in list_characters_in_tweet_text:
                    if len(elem) > 2:
                        x15[time_count] += 1
                        break       

    for i in range(0, len(x1)-1):
        x6.append(0); x7.append(0) 
    
    get_delta(x1,x6,2); get_delta(x6,x7,2)
    fin.close()  


# function to fit a model with features made and draw scatter plots
def regression_model(X,y):

    # create feature matrix
    X=np.column_stack((x1[0:len(x1)-1], x2[0:len(x1)-1], x3[0:len(x1)-1], x4[0:len(x1)-1], x5[0:len(x1)-1], 
        x6[0:len(x1)-1], x7[0:len(x1)-1], x8[0:len(x1)-1], x9[0:len(x1)-1], x10[0:len(x1)-1], x11[0:len(x1)-1], 
        x12[0:len(x1)-1], x13[0:len(x1)-1], x14[0:len(x1)-1], x15[0:len(x1)-1]))    
    
    # create target vector
    num_tweets_next_hour = x1[1:len(x1)]
    y=np.transpose(num_tweets_next_hour)
    X = sm.add_constant(X)
    
    # linear regression
    model = sm.OLS(y,X)
    results = model.fit()
    print(results.summary())    

    plt.scatter(x1[0:len(x1)-1],y); 
    plt.xlim(0,200); plt.ylim(0, 200); 
    plt.xlabel('x1 (number of tweets)'); plt.show()
    plt.scatter(x1[0:len(x1)-1],y); plt.xlabel('x1 (number of tweets)');  plt.show()    
    plt.scatter(x2[0:len(x1)-1],y); plt.xlabel('x2 (total number of retweets)'); plt.show()
    #plt.scatter(x2[0:len(x1)-1],y); plt.xlim(0,1500); plt.ylim(0,1000); plt.xlabel('x2 (total number of retweets)'); plt.show()
    plt.scatter(x3[0:len(x1)-1],y); plt.xlabel('x3 (sum of the numbers of followers)'); plt.show()
    #plt.scatter(x3[0:len(x1)-1],y); plt.xlim(0,300000); plt.ylim(0,300); plt.xlabel('x3 (sum of the numbers of followers)'); plt.show()
    plt.scatter(x4[0:len(x1)-1],y); plt.xlabel('x4 (max number of followers)'); plt.show()
    #plt.scatter(x4[0:len(x1)-1],y); plt.xlim(0,5000); plt.ylim(0,50); plt.xlabel('x4 (max number of followers)'); plt.show()
    plt.scatter(x5[0:len(x1)-1],y); plt.xlabel('x5 (time of the day)'); plt.show()
    plt.scatter(x6[0:len(x1)-1],y); plt.xlabel('x6 (time derivative)'); plt.show()
    #plt.scatter(x6[0:len(x1)-1],y); plt.xlim(0,200); plt.ylim(0,500); plt.xlabel('x6 (time derivative)'); plt.show()
    plt.scatter(x7[0:len(x1)-1],y); plt.xlabel('x7 (time accelaration'); plt.show()
    # plt.scatter(x7[0:len(x1)-1],y); plt.xlim(0,20); plt.ylim(0,500); plt.xlabel('x7 (time accelaration'); plt.show()
    plt.scatter(x8[0:len(x1)-1],y); plt.xlabel('x8 (number of mentions)'); plt.show()
    plt.scatter(x8[0:len(x1)-1],y); plt.xlim(0,100); plt.ylim(0,150); plt.xlabel('x8 (number of mentions)'); plt.show()
    plt.scatter(x9[0:len(x1)-1],y); plt.xlabel('x9 (url ratio)'); plt.show()
    plt.scatter(x10[0:len(x1)-1],y); plt.xlabel('x10 (passitivity_total)'); plt.show()
    plt.scatter(x10[0:len(x1)-1],y); plt.xlim(0,100); plt.ylim(0,60); plt.xlabel('x10 (passitivity_total)'); plt.show()
    plt.scatter(x11[0:len(x1)-1],y); plt.xlabel('x11 (passitivity_average)'); plt.show()
    plt.scatter(x12[0:len(x1)-1],y); plt.xlabel('x12 (passitivity_max)'); plt.show()
    # plt.scatter(x12[0:len(x1)-1],y); plt.xlim(0,200); plt.ylim(0,1000); plt.xlabel('x12 (passitivity_max)'); plt.show()
    plt.scatter(x13[0:len(x1)-1],y); plt.xlabel('x13 (co-occurence times with other hashtags)'); plt.show()
    plt.scatter(x13[0:len(x1)-1],y); plt.xlim(0,100); plt.ylim(0,50); plt.xlabel('x13 (co-occurence times with other hashtags)'); plt.show()
    plt.scatter(x14[0:len(x1)-1],y); plt.xlabel('x14 (case-sensitive hashtag count)'); plt.show()
    #plt.scatter(x14[0:len(x1)-1],y); plt.xlim(0,50); plt.ylim(0,50); plt.xlabel('x14 (case-sensitive hashtag count)'); plt.show()
    plt.scatter(x15[0:len(x1)-1],y); plt.xlabel('x15 (special signals)'); plt.show()
    #plt.scatter(x15[0:len(x1)-1],y); plt.xlim(0,40); plt.ylim(0,300); plt.xlabel('x15 (special signals)'); plt.show()

X = np.array([]); y=np.array([]);

#get_features('./tweet_data/tweets_#gopatriots.txt')
#get_features('./tweet_data/tweets_#patriots.txt')
#get_features('./tweet_data/tweets_#superbowl.txt')
#get_features('./tweet_data/tweets_#nfl.txt')
#get_features('./tweet_data/tweets_#gohawks.txt')
get_features('./tweet_data/tweets_#sb49.txt')

regression_model(X, y)

def main(argv):
    if len(argv) != 1 + 1:
        print >> sys.stderr, 'Usage : %s Target.txt' % (argv[0],)
        return -1
    
    get_features(argv[1])
    regression_model(X, y)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
