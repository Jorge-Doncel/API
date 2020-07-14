from src.app import app
from pymongo import MongoClient
from src.config import DBURL
from flask import request
from bson.json_util import dumps
from bson.objectid import ObjectId


client = MongoClient(DBURL)
print(f"connected to db {DBURL}")
db = client.get_default_database()


@app.route("/chat/create/<name>")
def create_user(name):
    """"
    Add a new user in the database
    """
    new_user= {"name": name}
    pre_user= db.user.distinct("name")
    if name in pre_user:
        raise ValueError ("This username already exists. Add another username.")
    else:
        add_user = db.user.insert_one(new_user)
        return dumps(f"New user create! user_name:{name}, user_id: {add_user.inserted_id} ")


@app.route("/chat/create")
def create_chat():
    """
    Create a chat in the database with all the participants (as Array)
    """
    chat_participants= request.args.getlist("participants")
    conver_name= request.args.get("chat_name")
    check_conver= list(db.conversation.find({"conversation_name":conver_name}))
    if len(check_conver) > 0:
        raise ValueError ("This chat was already added")
    else:
        add_participants = db.conversation.insert({"conversation_name":conver_name, "participants": chat_participants}) 
        return dumps(f'New chat create! Conversation id: {add_participants}')

@app.route("/chat/<conversation_id>/adduser")
def add_user(conversation_id):
    """
    Add a new user to a conversation
    """
    new_user= request.args.get("user_name")
    check_user= list(db.conversation.find({"_id": ObjectId(conversation_id), "participants":new_user}))
    if len(check_user) > 0:
        raise ValueError ("This username already added in this conversation.")
    else:
        add_user= db.conversation.update({"_id": ObjectId(conversation_id)},{"$push": {"participants": new_user}})
        return dumps(f"New user added to a conversation! user_id: {new_user}, conversation_id: {conversation_id} ")


@app.route("/chat/<conversation_id>/addmessage", methods=['POST'])
def add_message(conversation_id):
    """
    Add a message of a user in the database and in a specific conversation
    """
    conver= request.form.get("conversation_id")
    user= request.form.get("user_name")
    mensaje= request.form.get("message")
    check_user= list(db.conversation.find({"_id": ObjectId(conversation_id), "participants":user}))
    if len(check_user) == 0:
        raise ValueError ("This username is not in this conversation. Please, check again the conversation and user id")
    else:
        add_message= db.chatItem.insert({"conversation_id":ObjectId(conversation_id), "user_id": user, "message":f'{mensaje}'})
        return dumps(f"New Message added. Id message: {add_message}")

@app.route("/chat/<conversation_id>/list")
def check_message(conversation_id):
    """
    Get a list of all message of a user
    """
    all_message= db.chatItem.find({"conversation_id": ObjectId(conversation_id)}, {"message":1, "_id":0})
    json_message= dumps(db.chatItem.find({"conversation_id": ObjectId(conversation_id)}, {"user_id":1,"message":1, "_id":0}))
    return json_message

