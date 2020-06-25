from .utils import setDriver, createStorage, completeLink, scroll
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import datetime
import os


def twi_hashtag_originator(hashtag, minYear = 2006):
    # cache the hashtag for future use (screenshot)
    cache = "_".join(hashtag.split(" ")).replace("#", "")
    
    # checking wether argument is valid
    if hashtag is None or hashtag == "":
        print("Wrong argument: ", hashtag)
        return None

    # separate the words and remove #
    h = [j for j in hashtag.split(" ") if j != ""]
    check = lambda x: x[1:] if x.startswith("#") else x
    h = [check(j).lower() for j in h]

    # forming the URL part
    hashtag = f"(%23{h[0]}"
    for rest in h[1:]:
        hashtag += f" AND %23{rest}"
    hashtag += ")"
    
    # preliminary code
    soup = BeautifulSoup("", "html.parser")
    createStorage("twitter")
    screen = False
    
    # close driver as soon as work done
    with setDriver(headless = False) as driver:
        wait = WebDriverWait(driver, 3)
        year = minYear

        # checking if hashtag is actually ever been used
        url = f"https://twitter.com/search?q={hashtag}"
        driver.get(url)
        articles = returnAllTweets(wait)
        if len(articles) == 0:
            print("Hashtag has not been used in any tweets that are public")
            return None

        # check starting from minYear
        articles = []
        while(len(articles) == 0):
            url = f"https://twitter.com/search?q={hashtag}%20until%3A{str(year)}-01-01&src=typed_query"
            driver.get(url)
            articles = returnAllTweets(wait)
            year += 1
        scroll(driver, fastScroll = False)
        ti = returnAllTweets(wait)
        
        if len(ti) == 0:
            print("Something went wrong.")
            return None

        # remove tweets not containing the hashtag (This occurs if the tweet is a parent tweet of the hashtag containing tweet)
        t = []
        for post in ti:
            inner = post.get_attribute("innerHTML").lower()
            good = True
            for each in h:
                if f">#{each}</a>" not in inner:
                    good = False
                    break
            if good:
                t.append(post)

        # sort all posts by retrieving the timestamp
        timed = []
        for post in t:
            try:
                s = post.find_element_by_xpath('.//time')
                s = s.get_attribute("datetime")
                if s:
                    try:
                        timed.append({
                            "timestamp": datetime.datetime.strptime(s,"%Y-%m-%dT%H:%M:%S.%fZ"),
                            "elem": post
                        })
                    except:
                        pass
            except NoSuchElementException:
                pass
        t = sorted(timed, key = lambda x: x["timestamp"])
        
        # element of earliest post selected and screenshot taken
        if len(t) == 0:
            print("Something is seriously wrong")
            return None
        
        t = t[0]["elem"]
        try:
            with open(f"data/twitter/{cache}.png", "wb") as filex:
                filex.write(t.screenshot_as_png)
            screen = True
        except:
            print("Screenshot was unsuccessfull")
        t = t.get_attribute("innerHTML")
        soup = BeautifulSoup(t, "html.parser")
    
    result = {
        "poster": {
            "full_name": "",
            "username": "",
            "url": "",
            "id": "",
            "profile_image_url": ""
        },
        "timestamp": "",
        "post_link": "",
        "post_text": "",
        "embed": "",
        "screenshot": ""
    }
    a = soup.find("a")
    if a:
        result["poster"]["url"] = completeTwitterLink(a.get('href', ""))
        result["poster"]["username"] = result["poster"]["url"].replace("https://www.twitter.com/", "")
        k = a.findNext("a", {"href": a.get("href", "")})
        if k:
            result["poster"]["full_name"] = k.text.partition("@")[0]
        k = a.find("img")
        if k:
            result["poster"]["profile_image_url"] = k.get("src", "")
    a = soup.find(lambda tag: tag.name == 'a' and tag.find("time"))
    if a:
        link = completeTwitterLink(a.get("href", ""))
        result["post_link"] = link
        result["embed"] = f'<blockquote class="twitter-tweet"><a href="{link}"></a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
        k = a.find("time")
        if k:
            result["timestamp"] = k.get("datetime", "")
        soup = BeautifulSoup(str(soup).partition(str(a))[2], "html.parser")
        result["post_text"] = " ".join([s.text for s in soup.find_all("span")])
    if screen:
        result["screenshot"] = os.getcwd() + f"/data/twitter/{cache}"
    return result

def returnAllTweets(wait):
    try:
        return wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@data-testid="tweet"]')))
    except TimeoutException:
        return []

def completeTwitterLink(link):
    return completeLink(link, "https://www.twitter.com/")
