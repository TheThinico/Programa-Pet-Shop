class Tutor:
    def __init__(self,nome,telefone,email,cpf,endereco):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.cpf = cpf
        self.endereco = endereco

    def to_dict(self):
        return {
            "nome": self.nome,
            "telefone": self.telefone,
            "email": self.email,
            "cpf": self.cpf,
            "endereco": self.endereco
        }
    def set_dict(self,dict):
        self.nome = dict["nome"]
        self.telefone = dict["telefone"]
        self.email = dict["email"]
        self.cpf = dict["cpf"]
        self.endereco = dict["endereco"]

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

    def set_dict(self,dict):
        self.nome = dict["nome"]
        self.tipo = dict["tipo"]
        self.raca = dict["raca"]
        self.idade = dict["idade"]
        self.tutor_cpf = dict["tutor_cpf"]