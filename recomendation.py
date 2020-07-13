from sklearn.feature_extraction.text import CountVectorizer
from src.app import app
from pymongo import MongoClient
from src.config import DBURL
from flask import request
from bson.json_util import dumps
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity as distance
import numpy as np



client = MongoClient(DBURL)
print(f"connected to db {DBURL}")
db = client.get_default_database()
message= list(db.chatItem.find({},{"_id":0, "user_id": 1,"message":1}))

def create_dict():
    vacio={}
    for i in message:
        vacio[i["user_id"]] = vacio.get(i["user_id"], [])+ [i["message"]]

    lista=[]
    for k,v in vacio.items():
        lista.append((k, " ".join(v)))
    return dict(lista)

@app.route("/recomendation/<name>")
def recomendation(name):
    all_messages= create_dict()
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(all_messages.values())
    m = sparse_matrix.todense()
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix, 
                  columns=count_vectorizer.get_feature_names(), 
                  index=all_messages.keys())
    similarity_matrix = distance(df,df)
    sim_df = pd.DataFrame(similarity_matrix, columns=all_messages.keys(), index=all_messages.keys())
    np.fill_diagonal(sim_df.values, 0)
    re = sim_df[name].nlargest(3)
    return dumps(f'{name} is similar to {re.index[0]}, {re.index[1]} and {re.index[2]} ')