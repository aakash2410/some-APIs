import json
import requests
import string
import random
import pandas as pd 

count = 500
#Load the API-KEY into a variable so as to not leak it 
with open('YOU-API/you-API.txt', 'r') as f:
    API_KEY = f.read()
#Initialize the column lists
videoIds = []  
list_of_links = []                    
views =[]
likes = []
dislikes = []
commentCount=[]
publishedAt = []
#Start hitting the youtube search API for random videos according to the random search query generated as 'que'
for i in range(20):
    que = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))      #random search query name generated

    base_url ='https://www.googleapis.com/youtube/v3/search?maxResults={}&q={}&key={}'.format(count,que,API_KEY)
    response = requests.get(base_url)           #Hits

    data = response.json()
    for i in range(30):
        if data['items'][i]['id']['kind'] == 'youtube#video':
            videoIds.append(data['items'][i]['id']['videoId'])
        else:
            continue
#appending in the link column
for videoId in videoIds:
    list_of_links.append('https://www.youtube.com/watch?v=' + videoId)
#Hitting a new API link to get stats and snippets
for i in range(len(videoIds)):
    source = 'https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={}&key={}'.format(videoIds[i], API_KEY)
    response_new = requests.get(source)
    data = response_new.json()
    views.append(int(data['items'][0]['statistics']['viewCount']))
    try :
        likes.append(int(data['items'][0]['statistics']['likeCount']))
    except KeyError:
        likes.append(0)
    try:
        dislikes.append(int(data['items'][0]['statistics']['dislikeCount']))
    except KeyError:
        dislikes.append(0)
    publishedAt.append(data['items'][0]['snippet']['publishedAt'])
    try:
        commentCount.append(int(data['items'][0]['statistics']['commentCount']))
    except KeyError:
        commentCount.append(0)
#making a dictionary to store all with column names
df = {'video_link':list_of_links,
      'video_views': views,
      'upload_date': publishedAt,
      'comments': commentCount,
      'likes': likes, 
      'dislikes': dislikes}
#Converting to a DataFrame
df_new = pd.DataFrame(df)
#Converting to a csv and then saving it as well
df_new.to_csv('YoutubeData.csv')
