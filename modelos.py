class Tutor:
    cpf = ""
    nome = ""
    idade = ""
    sexo = ""

    telefone = ""
    email = ""

    endereco  = ""

    def __repr__(self):
        return f"{self.nome}, {self.idade} anos"

    def to_dict(self):
        return {
            "cpf": self.cpf,
            "nome": self.nome,
            "idade": self.idade,
            "sexo": self.sexo,
            "telefone": self.telefone,
            "email": self.email,
            "endereco": self.endereco
        }

    def set_dict(self,dados):
        self.cpf = dados["cpf"]
        self.nome = dados["nome"]
        self.idade = dados["idade"]
        self.sexo = dados["sexo"]

        self.telefone = dados["telefone"]
        self.email = dados["email"]

        self.endereco = dados["endereco"]

    def set_dados(self,cpf,nome,idade,sexo,telefone,email,endereco):
        self.cpf = cpf
        self.nome = nome
        self.idade = idade
        self.sexo = sexo

        self.telefone = telefone
        self.email = email

        self.endereco = endereco

class Animal:
    nome = ""
    tipo = ""
    raca = ""
    idade = ""

    tutor_cpf = ""

    def to_dict(self):
        return {
            "nome": self.nome,
            "tipo": self.tipo,
            "raca": self.raca,
            "idade": self.idade,
            "tutor_cpf": self.tutor_cpf,
        }

    def set_dict(self,dados):
        self.nome = dados["nome"]
        self.tipo = dados["tipo"]
        self.raca = dados["raca"]
        self.idade = dados["idade"]

        self.tutor_cpf = dados["tutor_cpf"]

    def set_dados(self, nome, tipo, raca, idade,tutor_cpf):
        self.nome = nome
        self.tipo = tipo
        self.raca = raca
        self.idade = idade

        self.tutor_cpf = tutor_cpf

class Funcionario:
    cpf = ""
    nome = ""
    idade = ""
    sexo = ""

    telefone = ""
    email = ""

    endereco = ""

    funcao = ""
    status = ""

    def to_dict(self):
        return {
            "cpf": self.cpf,
            "nome": self.nome,
            "idade": self.idade,
            "sexo": self.sexo,

            "telefone": self.telefone,
            "email": self.email,

            "endereco": self.endereco,

            "funcao": self.funcao,
            "status": self.status
        }

    def set_dict(self, dados):
        self.cpf = dados["cpf"]
        self.nome = dados["nome"]
        self.idade = dados["idade"]
        self.sexo = dados["sexo"]

        self.telefone = dados["telefone"]
        self.email = dados["email"]

        self.endereco = dados["endereco"]

        self.funcao = dados["funcao"]
        self.status = dados["status"]

    def set_dados(self, cpf, nome, idade, sexo, telefone, email, endereco, funcao, status):
        self.cpf = cpf
        self.nome = nome
        self.idade = idade
        self.sexo = sexo

        self.telefone = telefone
        self.email = email

        self.endereco = endereco

        self.funcao = funcao
        self.status = status
