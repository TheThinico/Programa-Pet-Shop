# app/dominio/agendamento.py
class Agendamento:
    def __init__(self, pet_nome: str, servico_nome: str, data: str, horario: str):
        self.pet_nome = pet_nome
        self.servico_nome = servico_nome
        self.data = data
        self.horario = horario

    def to_dict(self):
        return {
            "pet_nome": self.pet_nome,
            "servico_nome": self.servico_nome,
            "data": self.data,
            "horario": self.horario
        }
