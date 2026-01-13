import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def obter_banco():
    uri = os.getenv("MONGO_URI")

    print("DEBUG MONGO_URI ->", uri)  # 👈 diagnóstico

    if not uri:
        raise RuntimeError("MONGO_URI não definida no .env")

    client = MongoClient(uri)
    return client["petshop"]
