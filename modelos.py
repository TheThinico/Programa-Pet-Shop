import banco_de_dados

class Tutor:
    nome = "nome"
    telefone = "0"
    email = "email"
    cpf = "0"

    def __init__(self,nome,telefone,email,cpf):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.cpf = cpf

    def to_dict(self):
        return {
            "nome": self.nome,
            "telefone": self.telefone,
            "email": self.email,
            "cpf": self.cpf,
        }

class Animal:
    def __init__(self,nome,tipo,raca,idade,tutor_cpf):
        self.nome = nome
        self.tipo = tipo
        self.raca = raca
        self.idade = idade
        self.tutor_cpf = tutor_cpf

    def to_dict(self):
        return {
            "nome": self.nome,
            "tipo": self.tipo,
            "raca": self.raca,
            "idade": self.idade,
            "tutor_cpf": self.tutor_cpf,
        }
