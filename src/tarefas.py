from datetime import datetime, timedelta

class Tarefa:
    def __init__(self, titulo, descricao, prioridade, prazo):
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade
        self.prazo = datetime.strptime(prazo, "%Y-%m-%d").date()
        self.concluida = False
        self.tipo = "comum"

class TarefaUrgente(Tarefa):
    def __init__(self, titulo, descricao, prazo):
        # Adicione validação de prazo (ex: máximo 24h)
        data_prazo = datetime.strptime(prazo, "%Y-%m-%d").date()
        hoje = datetime.now().date()
        
        if (data_prazo - hoje) > timedelta(days=1):
            raise ValueError("Tarefa urgente deve ter prazo máximo de 24h!")
            
        super().__init__(titulo, descricao, "alta", prazo)
        self.tipo = "urgente"
