from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient 

app = Flask(__name__)

client = MongoClient("mongodb+srv://sparta:jungle@cluster0.oxcto9l.mongodb.net/?retryWrites=true&w=majority")
db = client.dbjungle

## HTML 
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/memo", methods=["GET"])
def listing():
    #1. find all documents and exclude the id key's value
    all_docs = list(db.memos.find({}, {"_id":False}))
    #2. lay out book info based on articles key values
    for title in all_docs:
        print(title) 
    return jsonify({"result":"success", "msg":"GET connected successfully!"})

@app.route("/", methods=["POST"])
def post_articles():
    #1. receive data from client
    url_receive = request.form["url_give"]
    comment_receive = request.form["comment_give"]

    #2. scrape meta tags
    url = 'https://platum.kr/archives/120958'
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.txt, "html.parser")

    og_image = soup.select_one("meta[property='og:iamge']")
    og_title = soup.select_one("meta[property='og:title']")
    og_description = soup.select_one("meta[property='og:description']")

    url_title = og_title["content"]
    url_description = og_description["content"]
    url_image = og_image["content"]

    article = {
        "url": url_receive,
        "title": url_title,
        "desc": url_description,
        "image": url_image,
        "comment": comment_receive
    }

    #3. record the data to MongoDB
    db.articles.insert_one(article)

    return jsonify({"result": "success", "msg":"POST connnected successfully!"})


