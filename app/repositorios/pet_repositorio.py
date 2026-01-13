# app/repositorios/pet_repositorio.py
from app.banco_dados.conexao import obter_banco

class PetRepositorio:
    def __init__(self):
        self.db = obter_banco()
        self.colecao = self.db["pets"]

    def inserir(self, pet):
        return self.colecao.insert_one(pet.to_dict())

    def listar(self):
        return list(self.colecao.find({}, {"_id": 0}))
