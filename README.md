# Twisearch
Added functionality to get profile information for a twitter user, and to get the first post for a list of hashtags.

## Install

1. For dependencies:  
```bash
python -m pip install selenium bs4 datetime
```
2. Download the chromedriver from [here](https://chromedriver.chromium.org/downloads)
3. Open the file *twisearch.py* and set the variable EXECUTABLE_PATH to the path where the driver is downloaded.

## Twitter Search

### Code

```python
from twisearch import twitterSearch

results = twitterSearch("Pakistan News")
print(results)
```

### Ouput

```
[{'id': '18140095',
  'username': 'paknews',
  'name': 'Pakistan News',
  'media_directory': 'https://pbs.twimg.com/profile_images/1737791275/Flag-of-Pakistan-256_bigger.png'},
 {'id': '54246210',
  'username': 'NewsInsider',
  'name': 'Latest Pakistan News',
  'media_directory': 'https://pbs.twimg.com/profile_images/303756524/images_bigger.jpeg'},
 {'id': '480682661',
  'username': 'PakistanWeekly',
  'name': 'Pakistan Weekly News',
  'media_directory': 'https://pbs.twimg.com/profile_images/2341730932/8l4e9321u5tzme9a333s_bigger.jpeg'}]
```

## Twitter User Profile Info

### Code

```python
from twiuser import twitter_profile

results = twitterSearch("reddit")
print(results)
```

### Ouput

```
{'id': '811377',
 'profile_image_url': 'https://pbs.twimg.com/profile_images/1267872080797696002/5hv6hTuL_400x400.jpg',
 'Full_name': 'Reddit',
 'bio_data': 'The front page of the internet  •  Get the app: http://reddit.com/mobile/download\xa0 • Interested in doing an AMA? Visit http://redditinc.com/ama\xa0',
 'location': 'San Francisco, CA',
 'website': 'http://reddit.com',
 'join_date': 'Joined March 2007',
 'Tweets': '77,394 Tweets',
 'Following': '558 Following',
 'Followers': '712,742 Followers',
 'Likes': '10,706 Likes',
 'Lists': '',
 'moments': '1 Moment'}
```

## Twitter Hashtag Originator

### Code

```python
from hastag_originator import twi_hashtag_originator

result = twi_hashtag_originator("pia planecrash", minYear = 2006)
print(result)
```

### Output

```
{'poster': {'full_name': '*Muhammad Uzair*', 'username': 'MadaniMsgs', 'url': 'https://www.twitter.com/MadaniMsgs', 'id': '', 'profile_image_url': 'https://pbs.twimg.com/profile_images/3247532514/06228b921421d7155ade3467ed6ebb52_bigger.jpeg'},
'timestamp': '2012-04-21T00:53:25.000Z',
'post_link': 'https://www.twitter.com/MadaniMsgs/status/193502667727835136',
'post_text': '#PIA   operating special flight today 7 am for immediate  #family  members of  #BhojaAir  affectees.  http://    #planecrash    #bhojaair',
'embed': '<blockquote class="twitter-tweet"><a href="https://www.twitter.com/MadaniMsgs/status/193502667727835136"></a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>',
'screenshot': '/home/sascs/sacas/data/twitter/pia_planecrash'}
```
