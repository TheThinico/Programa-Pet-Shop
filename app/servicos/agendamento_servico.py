# app/servicos/agendamento_servico.py
class AgendamentoServico:
    def validar(self, data, horario):
        if not data or not horario:
            raise ValueError("Data e horário são obrigatórios")
