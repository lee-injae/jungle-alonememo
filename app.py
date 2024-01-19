from dotenv import load_dotenv
load_dotenv()

import os 

mongo_uri = os.getenv('MONGO_URI')

from pymongo import MongoClient

client = MongoClient(mongo_uri)
db = client.db_jungle

from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/memo", methods=["POST"])
def post_article():
    # 1. Receive JSON data from client
    data = request.json
    url_receive = data.get("url_give")
    comment_receive = data.get("comment_give")

    print(url_receive)
    print(comment_receive)

    #2. scrape meta tags
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, "html.parser")

    og_image = soup.select_one("meta[property='og:image']")
    og_title = soup.select_one("meta[property='og:title']")
    og_description = soup.select_one("meta[property='og:description']")

    url_title = og_title["content"] if og_title else "No title found"
    url_description = og_description["content"] if og_description else "no description found"
    url_image = og_image["content"] if og_image else "default-image-url"

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

@app.route("/memo", methods=["GET"])
def read_articles():
    #1. find all documents and exclude the id key's value
    result = list(db.articles.find({}, {"_id": 0}))
    #2. lay out book info based on articles key values
    return jsonify({"result": "success", "articles": result})

if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)