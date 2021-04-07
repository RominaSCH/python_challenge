import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"

# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"


db = {}
detail_db = {}
app = Flask("DayNine")

@app.route("/")#flask 는 참 어렵네요 쓰앵..
def index():
  order_by = request.args.get("order_by","popular")#주소에 있는 제출값
  if order_by not in db:#db안에 order 없을경우
    if order_by == "popular":
      news = requests.get(popular)
    elif order_by == "new":
      news = requests.get(new)
    results = news.json()["hits"]
    db[order_by] = results
  else:#db안에 있을경우
    results = db[order_by]
  return render_template("index.html", order_by=order_by, results=results)# html {{}} 변수명 = 파이썬 변수명

@app.route("/<id>")
def detail(id):#디테일도 db에 넣고 빨리빨리 이동해주고 싶다
  if id not in detail_db:
    detail_request = requests.get(make_detail_url(id))
    result = detail_request.json()
    detail_db[id]=result
  else:
    result = detail_db[id]
  return render_template("detail.html", result=result)

app.run(host="0.0.0.0")
