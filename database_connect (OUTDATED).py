from http.cookiejar import user_domain_match

import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

user_name = "thiago"
pass_word = "mPKueWWlKg2MsWhk"

uri = f"mongodb+srv://{user_name}:{pass_word}@cluster0.164lard.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

mydb = client["banco"]
mycol = mydb["cadastro"]

dicionario  = [
        {"_id": "33377722211","nome": "Andre", "idade" : "89"},
        {"_id": "11122233344","nome": "Maria", "idade" : "38"}]

try:
    x = mycol.insert_many(dicionario)
    print(x)
    print(x.inserted_ids)
except:
    print("ERRO: dados não foram cadastrados")

