'''
Created on 2/06/2017

@author: hamid.moghaddam
'''

import feedparser
import json
import os

from flask import Flask
from flask import request
from flask import make_response
# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)
    print(res)
    res = json.dumps(res, indent=4)
    
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    #print(r)
    return r
def processRequest(req):
    if req.get("result").get("action") == "news.search":
        titles[:]=[]
        contents[:]=[]
        return read_news_title()
    elif req.get("result").get("action") == "article.open":
        return get_text(req)
    else:
        return {}
def read_news_title():
    feed = feedparser.parse("http://www.stuff.co.nz/rss/")
    
    for post in feed.entries:
        titles.append(post.title)
        contents.append(post.content)
    res= makeWebhookResult(titles[0:3])
    return res
def get_text(req):
    result = req.get("result")
    parameters = result.get("parameters")
    number = parameters.get("number")
    if number is None:
        return None    
    speech= contents[number]
    return {
        "speech": speech,
        "displayText": speech,
        "data": {},
        "contextOut": [],
        "source": "Fairfax Chatbot"
    }    
def makeWebhookResult(data):
    speech=""
    for i in range(0,len(data)):    
        speech +=str(i+1)+". "+data[i]+". "
    #print("Response:")
    #print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data": {},
        "contextOut": [],
        "source": "Fairfax Chatbot"
    }    
if __name__ == '__main__':
    titles=[]
    contents=[]
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
    