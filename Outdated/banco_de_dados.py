from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#selecionando banco de dados e insere os dados na tabela
def set_database_datas(dictionary_data):
    mydb = client["banco"]
    mycol = mydb["cadastro"]

    # dicionario  = [
    #         {"nome": "Andre", "idade" : "89"},
    #         {"nome": "Maria", "idade" : "38"}]

    try:
        x = mycol.insert_many(dictionary_data)
        print(x)
        print(x.inserted_ids)
    except:
        print("ERRO: dados não foram cadastrados")


uri = "mongodb+srv://thiago:mPKueWWlKg2MsWhk@cluster0.164lard.mongodb.net/?appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

