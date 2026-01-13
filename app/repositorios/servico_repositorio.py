# app/repositorios/servico_repositorio.py
from app.banco_dados.conexao import obter_banco

class ServicoRepositorio:
    def __init__(self):
        self.db = obter_banco()
        self.colecao = self.db["servicos"]

    def inserir(self, servico):
        return self.colecao.insert_one(servico.to_dict())

    def listar(self):
        return list(self.colecao.find({}, {"_id": 0}))
