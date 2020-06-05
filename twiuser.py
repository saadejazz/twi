import requests
from bs4 import BeautifulSoup
from json import JSONDecodeError

############################ Usage #####################
# from twiuser import twitter_profile
# username = "realDonaldTrump"
# print(twitter_profile(username))
########################################################

def twitter_profile(username):
    
    # data structure for dict returned
    result = {
    "id": "",
    "profile_image_url": "",
    "Full_name": "",
    "bio_data": "",
    "location": "",
    "website": "",
    "join_date": "",
    "Tweets": None,
    "Following": None,
    "Followers": None,
    "Likes": None,
    "Lists": None,
    "moments": None
    }

    # check if valid argument given
    if type(username) != str or username == "":
        print("Invalid argument type")
        return result

    # headers to send with request
    headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": f"https://twitter.com/{username}",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
    "X-Twitter-Active-User": "yes",
    "X-Requested-With": "XMLHttpRequest",
    "Accept-Language": "en-US",
    }

    # send request and check if the profile exists
    k = requests.get(f"https://twitter.com/{username}", headers = headers)
    try:
        print(k.json().get('message'))
        return result
    except JSONDecodeError:
        pass
    
    # if profile exists, go forward with scraping
    soup = BeautifulSoup(k.text, "html.parser")
    d = soup.find('div', {'class': 'ProfileAvatar'})
    if d:
        d = d.find('a')
        if d:
            result["profile_image_url"] = d.get('href', '')
            result["Full_name"] = d.get('title', '')
    d = soup.find('p', {'class': 'ProfileHeaderCard-bio'})
    if d:
        result["bio_data"] = d.text
    d = soup.find('span', {'class': 'ProfileHeaderCard-urlText'})
    if d:
        d = d.find('a')
        if d:
            result["website"] = d.get('title', '')
    d = soup.find('span', {'class': 'ProfileHeaderCard-locationText'})
    if d:
        result["location"] = " ".join([a for a in d.text.replace("\n", "").split() if not a == ""])
    d = soup.find('span', {'class': 'ProfileHeaderCard-joinDateText'})
    if d:
        result["join_date"] = d.text
    d = soup.find('div', {'class': 'ProfileNav'})
    if d:
        result["id"] = d.get("data-user-id", "")
        cls = ["tweets", "following", "followers", "favorites", "lists", "moments"]
        keys = list(result.keys())[7:]
        for i in range(len(cls)):
            s = d.find('li', {'class': f'ProfileNav-item--{cls[i]}'})
            if s:
                a = s.find('a')
                if a:
                    result[keys[i]] = a.get('title')
    return result
