from src.app import app
from pymongo import MongoClient
from src.config import DBURL
from flask import request
from bson.json_util import dumps
from bson.objectid import ObjectId
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


client = MongoClient(DBURL)
print(f"connected to db {DBURL}")
db = client.get_default_database()
sia = SentimentIntensityAnalyzer()

@app.route("/chat/<conversation_id>/sentiment")
def sentiment(conversation_id):
    """
    Get sentiments of all messages and user in a conversation
    """
    messages = list(db.chatItem.find({"conversation_id": ObjectId(conversation_id)},{"_id":0,"message":"1", "user_id":1}))
    if len(messages) == 0:
        raise ValueError ("Conversation id don't find. Please, introduce it again")
    else:
        return dumps([{"name": messages[i]["user_id"], "message": messages[i]["message"],"sentiments": sia.polarity_scores(messages[i]["message"])} for i in range(len(messages))])

@app.route("/chat/<conversation_id>/sentiment/<name>")
def sentiment_character(conversation_id, name):
    """
    Get sentiments of a user in a conversation
    """
    messages = list(db.chatItem.find({"conversation_id": ObjectId(conversation_id), "user_id": name},{"_id":0,"user_id":1,"message":"1"}))
    if len(messages) == 0:
        raise ValueError ("Name or conversation id don't find. Please, introduce it again")
    else:
        return dumps([{"name": messages[i]["user_id"], "message": messages[i]["message"],"sentiments": sia.polarity_scores(messages[i]["message"])} for i in range(len(messages))])

@app.route("/chat/<conversation_id>/sentiment/<name>/total")
def sentiment_character_total(conversation_id, name):
    """
    Get the sum of sentiments of a user in a conversation
    """
    messages = list(db.chatItem.find({"conversation_id": ObjectId(conversation_id), "user_id": name},{"_id":0,"message":"1"}))
    if len(messages) == 0:
        raise ValueError ("Name or conversation id don't find. Please, introduce it again")
    else: 
        total=[sia.polarity_scores(messages[i]["message"]) for i in range(len(messages))]
        suma= {k: round(sum(d[k] for d in total)/len(total),4) for k in total[0]}
        return dumps(f'{name} has {suma["neg"]} of negativity, {suma["neu"]} of neutral and {suma["pos"]} of positivity in this episode')

@app.route("/chat/sentiment/<name>")
def sentiment_character_allSeasons(name):
    """
    Get sentiments of a user in all the messages the user has
    """
    messages_name1 = list(db.chatItem.find({"user_id": name},{"_id":0,"message":"1"}))
    if len(messages_name1) == 0:
        raise ValueError ("Name don't find. Please, introduce it again")
    else:
        total_name1=[sia.polarity_scores(messages_name1[i]["message"]) for i in range(len(messages_name1))]
        suma_name1= {k: round(sum(d[k] for d in total_name1)/len(total_name1),4) for k in total_name1[0]}
        return dumps(f'{name} has {suma_name1["neg"]} of negativity, {suma_name1["neu"]} of neutral  in all the episodes')

@app.route("/chat/sentiment/<name1>/<name2>")
def sentiment_compare(name1, name2):
    """
    Compare 2 user sentiments across all messages
    """
    messages_name1 = list(db.chatItem.find({"user_id": name1},{"_id":0,"message":"1"}))
    messages_name2 = list(db.chatItem.find({"user_id": name2},{"_id":0,"message":"1"}))
    if len(messages_name1) == 0:
        raise ValueError ("First name don't find. Please, introduce it again")
    if len(messages_name2) == 0:
        raise ValueError ("Second name don't find. Please, introduce it again")
    else:
        total_name1=[sia.polarity_scores(messages_name1[i]["message"]) for i in range(len(messages_name1))]
        total_name2=[sia.polarity_scores(messages_name2[i]["message"]) for i in range(len(messages_name2))]
        suma_name1= {k: round(sum(d[k] for d in total_name1)/len(total_name1),4) for k in total_name1[0]}
        suma_name2= {k: round(sum(d[k] for d in total_name2)/len(total_name2),4) for k in total_name2[0]}
        return dumps(f'{name1} has {suma_name1["neg"]} of negativity, {suma_name1["neu"]} of neutral and {suma_name2["pos"]} and {name2} has {suma_name2["neg"]} of negativity, {suma_name2["neu"]} of neutral and {suma_name2["pos"]} in all the episodes')



