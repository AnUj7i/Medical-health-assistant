import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import pandas as pd

def init_firebase(config_path):
    if not firebase_admin._apps:
        cred = credentials.Certificate(config_path)
        firebase_admin.initialize_app(cred)
    return firestore.client()

def save_user_data(name, age):
    db = firestore.client()
    db.collection("users").add({
        "name": name,
        "age": age,
        "timestamp": datetime.datetime.now()
    })

def log_chat_to_firebase(user, query, response):
    db = firestore.client()
    db.collection("chats").add({
        "user": user,
        "query": query,
        "response": response,
        "timestamp": datetime.datetime.now()
    })

def get_analytics_data():
    db = firestore.client()
    chats = list(db.collection("chats").stream())
    data = []
    for chat in chats:
        d = chat.to_dict()
        data.append(d["query"])
    if not data:
        return pd.DataFrame()
    df = pd.DataFrame(data, columns=["query"])
    df = df["query"].value_counts().reset_index()
    df.columns = ["query", "count"]
    return df
