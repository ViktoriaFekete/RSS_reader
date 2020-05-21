from django.shortcuts import render
from django.http import HttpResponse
import feedparser
from datetime import datetime, date
import re


def index(request):

        feed_url = "https://www.sme.sk/rss-title"
        #orderby = "desc"

    # if request.GET.get("url", "orderby"):

       # feed_url = request.GET.get("url", False)
        feed = feedparser.parse(feed_url)
        # orderby = request.GET["orderby"]


        # if orderby == "asc":
        #     my_sorted_date = sorted(feed['entries'], key=lambda x: datetime.strptime(x['published'][5:25], '%d %b %Y %H:%M:%S'), reverse=False )
        # else:
        my_sorted_date = sorted(feed['entries'], key=lambda x: datetime.strptime(x['published'][5:25], '%d %b %Y %H:%M:%S'), reverse=True )
         
        feed['entries'] = my_sorted_date

        feed_length = len(feed['entries'])        
        posts = []

        for i in range(feed_length):
            key = feed['entries'][i]['published_parsed']
            published = datetime(key[0], key[1], key[2], key[3], key[4], key[5]) 
           
            try:
                value = feed['entries'][i].links[0]['href']
                image_url = re.search('http.?:.*(png|jpeg|jpg).rev=.*', value).group()

            except AttributeError:
                image_url = ""

            if (image_url == ""):
                try:
                    value = feed['entries'][i].summary_detail['value']
                    image_url = re.search('http.?:.*(png|jpeg|jpg)+(\?rev=.*)?', value).group()
                except:
                    image_url = ""


            posts.append({
                'title': feed['entries'][i].title,
                'description': feed['entries'][i].summary,
                'link': feed['entries'][i].link,
                'published': published,
                'image_url': image_url,
            })
    # else:
    #     feed = None

        return render(request, 'rss/reader.html', {

            'feed' : feed,
            'posts': posts,

        })

  
