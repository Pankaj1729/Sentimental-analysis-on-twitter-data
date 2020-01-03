import tkinter as tk
import sys, tweepy, csv, re
import textblob
from textblob import TextBlob
import matplotlib.pyplot as plt, mpld3

root = tk.Tk()
root.title("Tweeter Analysis")
root.minsize(600, 400)
root['bg']='light blue'

class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self, searchTerm, NoOfTerms):

        # enter your  authenticating detail here 
        #consumerKey = 
        #consumerSecret = 
        #accessToken = 
        #accessTokenSecret = 
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret
                              )
        api = tweepy.API(auth)

        # input for term to be searched and how many tweets to search

        # searchTerm = input("Enter Keyword/Tag to search about: ")
        # NoOfTerms = int(input("Enter how many tweets to search: "))

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang="en").items(NoOfTerms)

        # Open/create a file to append data to
        csvFile = open('result.csv', 'a')

        # Use csv writer
        csvWriter = csv.writer(csvFile)

        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0

        # iterating through tweets fetched
        for tweet in self.tweets:
            # Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1

        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        wpositive = self.percentage(wpositive, NoOfTerms)
        spositive = self.percentage(spositive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        wnegative = self.percentage(wnegative, NoOfTerms)
        snegative = self.percentage(snegative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        # finding average reaction
        polarity = polarity / NoOfTerms

        # printing out data

        label4['text']="How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets."
        label4.config(bg='white')
        # print()
        # print("General Report: ")

        if (polarity == 0):
            label5["text"]="Neutral"
            label5.config(bg='white')
        elif (polarity > 0 and polarity <= 0.3):
            label5["text"]="Weakly Positive"
            label5.config(bg='white')
        elif (polarity > 0.3 and polarity <= 0.6):
            label5["text"]="Positive"
            label5.config(bg='white')
        elif (polarity > 0.6 and polarity <= 1):
            label5["text"]="Strongly Positive"
            label5.config(bg='white')
        elif (polarity > -0.3 and polarity <= 0):
            label5["text"]="Weakly Negative"
            label5.config(bg='white')
        elif (polarity > -0.6 and polarity <= -0.3):
            label5["text"]="Negative"
            label5.config(bg='white')
        elif (polarity > -1 and polarity <= -0.6):
            label5["text"]="Strongly Negative"
            label5.config(bg='white')

        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(wpositive) + "% people thought it was weakly positive")
        print(str(spositive) + "% people thought it was strongly positive")
        print(str(negative) + "% people thought it was negative")
        print(str(wnegative) + "% people thought it was weakly negative")
        print(str(snegative) + "% people thought it was strongly negative")
        print(str(neutral) + "% people thought it was neutral")


        self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm,
                          NoOfTerms)

    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm,
                     noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]',
                  'Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]',
                  'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

        # plt.plot([3,1,4,1,5], 'ks-', mec='w', mew=5, ms=20)
        # mpld3.enable_notebook()
        # mpld3.show()


label1 = tk.Label(root, text="Enter Keyword/Tag to search about:", font='bold')
label1.grid(row=0, column=0,pady=20)
varmsg1 = tk.StringVar()
txtMsg1 = tk.Entry(master=root, textvariable=varmsg1,bg='silver')
txtMsg1.grid(row=0, column=1)
input1 = txtMsg1.get()

label2 = tk.Label(root, text="Enter how many tweets to search:", font='bold')
label2.grid(row=1, column=0,pady=10)
varmsg2 = tk.IntVar()
txtMsg2 = tk.Entry(master=root, textvariable=varmsg2,bg='silver')
txtMsg2.grid(row=1, column=1)
input2 = txtMsg2.get()
label4 = tk.Label(root, text="", font='bold',bg='light blue')
label4.grid(row=2, column=1,pady=10)
label3 = tk.Label(root, text="General Report:", font='bold')
label3.grid(row=3, column=0,pady=10)

label5 = tk.Label(root, text="", font='bold',bg='light blue')
label5.grid(row=3, column=1,pady=10)

def run():
    sa = SentimentAnalysis()
    sa.DownloadData(varmsg1.get(), varmsg2.get())


analysebtn = tk.Button(root, text="Do Analysis", width=15, command=run, font='bold', bg='light yellow')
analysebtn.grid(row=4, column=1,pady=20)

root.mainloop()
