from src.database import DatabaseManager
from src.tarefas import Tarefa, TarefaUrgente

class GerenciadorTarefas:
    def __init__(self):
        self.db = DatabaseManager()
        
    def inicializar(self):
        """Conecta ao banco e cria a tabela, se necessário."""
        self.db.conectar()  # Conecta ao banco
        self.db.criar_tabela()  # Cria a tabela se não existir

    def adicionar_tarefa(self, tarefa):
        query = """
            INSERT INTO tarefas (titulo, descricao, prioridade, prazo, tipo)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (tarefa.titulo, tarefa.descricao, tarefa.prioridade, tarefa.prazo, tarefa.tipo)
        self.db.executar_query(query, valores)

    def listar_tarefas(self, filtro_prioridade=None):
        query = "SELECT * FROM tarefas"
        if filtro_prioridade:
            query += f" WHERE prioridade = %s"
            return self.db.buscar_dados(query, (filtro_prioridade,))
        return self.db.buscar_dados(query)
    
    def marcar_concluida(self, id_tarefa):
        """Marca uma tarefa como concluída no banco de dados."""
        query = """
        UPDATE tarefas
        SET concluida = TRUE
        WHERE id = %s
        """
        self.db.executar_query(query, (id_tarefa,))

    def excluir_tarefa(self, id_tarefa: int, confirmar: bool = True):
        """Exclui uma tarefa específica, com confirmação se pendente"""
        tarefa = self.db.buscar_dados("SELECT * FROM tarefas WHERE id = %s", (id_tarefa,))
    
        if not tarefa:
            raise Exception("Tarefa não encontrada!")
    
        tarefa = tarefa[0]
    
        if confirmar and not tarefa['concluida']:
            # Lógica de confirmação será implementada na CLI
        
            # Se confirmado:
            self.db.executar_query("DELETE FROM tarefas WHERE id = %s", (id_tarefa,))
        else:
            self.db.executar_query("DELETE FROM tarefas WHERE id = %s", (id_tarefa,))

    def excluir_tarefas_concluidas(self):
        """Exclui todas as tarefas concluídas sem confirmação"""
        query = "DELETE FROM tarefas WHERE concluida = TRUE"
        linhas_afetadas = self.db.executar_query(query)
        return linhas_afetadas
