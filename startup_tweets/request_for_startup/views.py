from django.shortcuts import render
import twint
import pandas as pd

# Create your views here.

def index(request):
    return render(request, 'index.html')

def startup(request):
    startDate = request.GET.get('start date')
    endDate = request.GET.get('end date')
    count = request.GET.get('count')
    tw = twint.Config()
    tw.Search = "request for startup"
    tw.Limit = int(count)
    tw.Store_csv = True
    tw.Pandas = True
    tw.Output = "tweets.csv"

    tw.Since = startDate
    tw.Until = endDate

    twint.run.Search(tw)

    columns_to_keep = ['date', 'tweet', 'username', 'name', 'nlikes', 'nreplies', 'nretweets']
    Tweets_df = twint.storage.panda.Tweets_df
    Tweets_df = Tweets_df[columns_to_keep]
    Tweets_df = Tweets_df.sort_values(by=['nretweets','nlikes','nreplies','date'], ascending=False)
    Tweets_df.to_csv('tweets.csv', index=False)
    tweets_html = Tweets_df.to_html()
    context = {
        'output' : tweets_html
    }
    

    return render(request,'data.html', context)