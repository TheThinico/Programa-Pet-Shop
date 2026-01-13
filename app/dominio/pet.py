# app/dominio/pet.py
class Pet:
    def __init__(self, nome: str, especie: str, cliente_nome: str):
        self.nome = nome
        self.especie = especie
        self.cliente_nome = cliente_nome

    def to_dict(self):
        return {
            "nome": self.nome,
            "especie": self.especie,
            "cliente_nome": self.cliente_nome
        }
