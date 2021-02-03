from flask import Flask, render_template, request
from getData import getStories, getStory
app = Flask("Hacker News")

ORDERBY = 'order_by'
PAGE = 'page'
POPULAR = 'Popular'
NEW = 'New'

@app.route("/")
def home():
    order_by = request.args.get(ORDERBY)
    print(order_by)
    if (not order_by):
      order_by=POPULAR
    page = request.args.get(PAGE)
    print(page)
    if (not page):
        page = 1
    data = getStories(order_by, page)

    return render_template("home.html", data=data)

@app.route("/<id>")
def details(id):
    data = getStory(id)

    return render_template("details.html", data=data)


app.run(host="0.0.0.0")
