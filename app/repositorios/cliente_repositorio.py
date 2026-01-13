from app.banco_dados.conexao import obter_banco

class ClienteRepositorio:
    def __init__(self):
        self.db = obter_banco()
        self.colecao = self.db["clientes"]

    def inserir(self, cliente):
        return self.colecao.insert_one(cliente.to_dict())

    def listar(self):
        return list(self.colecao.find({}, {"_id": 0}))
