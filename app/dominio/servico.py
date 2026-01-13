# app/dominio/servico.py
class Servico:
    def __init__(self, nome: str, preco: float):
        self.nome = nome
        self.preco = preco

    def to_dict(self):
        return {
            "nome": self.nome,
            "preco": self.preco
        }
