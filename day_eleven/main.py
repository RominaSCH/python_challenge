import requests
from flask import Flask, render_template, request
"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}
"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = ["programming", "javascript", "reactjs", "reactnative", "css", "Flask", "django", "golang", "flutter", "rust"]


# standard = [hot, now, today, week, month, year, all]

# -----------------scrapping------------------#


from bs4 import BeautifulSoup

headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}


def extract_each(reddit, subreddit):
    try:
        link_part = reddit.find(
            "a",
            {"class": "SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"})["href"]
        # link = "https://www.reddit.com" + link_part
        title = reddit.find("h3", {"class": "_eYtD2XCVieq6emjKBH3m"}).string
        votes = reddit.find("div", {"class": "_1rZYMD_4xY3gRcSS3p8ODO"}).string
    except:
        pass
    return {"votes": int(votes), "title": title, "link": link_part, "subreddit":subreddit}

# https://www.reddit.com/r/Python/top/?t=hour
# https://www.reddit.com/r/Python/top/?t=week
# https://www.reddit.com/r/Python/top/?t=month
# https://www.reddit.com/r/Python/top/?t=year
# https://www.reddit.com/r/Python/top/?t=all

def scrape_reddit(subreddit):
    rd = []
    url = f"https://www.reddit.com/r/{subreddit}/top/?t=montht"
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, "html.parser")

    all_reddits = soup.find("div", {"class": "rpBJOHq2PR60pnwJlUyP0"})
    each_reddit = all_reddits.find_all("div", {"class": "Post"})

    for reddit in each_reddit:
      try:
        extracted = extract_each(reddit, subreddit)
        rd.append(extracted)
      except:
        pass

    return rd

def sum_reddits(subreddits):#rd 모아서 votes순으로 정리해야함. 순서..?어떻게함...:?
  sum_rd = []
  for subreddit in subreddits:
    result = scrape_reddit(subreddit)
    sum_rd += result
  return sum_rd


# ---------------------flask---------------------#


app = Flask("Reddit Scrapping")

@app.route("/")
def home():
  return render_template("home.html", subreddits=subreddits)


@app.route("/read")
def read():
  options = []
  # reddits_final = []
  for subreddit in subreddits:
    if subreddit in request.args:
      options.append(subreddit)
  reddits_final = sum_reddits(options)
  #reddits_final 순서대로 정리해야함
  reddits_final.sort(key=lambda reddit: reddit["votes"], reverse=True)
  return render_template("read.html", rd=reddits_final, options=options)

app.run(host="0.0.0.0")