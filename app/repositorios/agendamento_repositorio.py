# app/repositorios/agendamento_repositorio.py
from app.banco_dados.conexao import obter_banco

class AgendamentoRepositorio:
    def __init__(self):
        self.db = obter_banco()
        self.colecao = self.db["agendamentos"]

    def inserir(self, agendamento):
        return self.colecao.insert_one(agendamento.to_dict())

    def listar(self):
        return list(self.colecao.find({}, {"_id": 0}))
