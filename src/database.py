import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.usuario = os.getenv('DB_USER')
        self.senha = os.getenv('DB_PASSWORD')
        self.banco = os.getenv('DB_NAME')
        self.conexao = None

    def conectar(self):
        try:
            self.conexao = mysql.connector.connect(
                host=self.host,
                user=self.usuario,
                password=self.senha,
                database=self.banco
            )
            return self.conexao
        except Error as e:
            print(f"ERRO DE CONEXÃO: {e}")
            return None

    def criar_tabela(self):
        if self.conexao is None:
            print("Erro: Nenhuma conexão com o banco!")
            return 

        criar_tabela_query = """
        CREATE TABLE IF NOT EXISTS tarefas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            descricao TEXT,
            prioridade ENUM('alta', 'media', 'baixa') NOT NULL,
            prazo DATE,
            concluida BOOLEAN DEFAULT FALSE,
            tipo VARCHAR(50)
        )
        """
        try:
            with self.conexao.cursor() as cursor:
                cursor.execute(criar_tabela_query)
                self.conexao.commit()
                print()
                print("Tabela 'tarefas' criada/verificada!")
        except Error as e:
            print()
            print(f"Erro ao criar tabela: {e}")
    
    def executar_query(self, query, parametros=None):
        if self.conexao is None:
            print("Erro: Nenhuma conexão com o banco!")
            return 0
            
        try:
            with self.conexao.cursor() as cursor:
                if parametros:
                    cursor.execute(query, parametros)
                else:
                    cursor.execute(query)
                self.conexao.commit()
                return cursor.rowcount  # Retorna o número de linhas afetadas
        except Error as e:
            print(f"Erro ao executar a query: {e}")
            return 0

    def ultima_linhas_afetadas(self):
        return self.conexao.cursor().rowcount if self.conexao else 0

    def buscar_dados(self, query, parametros=None):
        if self.conexao is None:
            print()
            print("Erro: Nenhuma conexão com o banco!")
            return []

        try:
            with self.conexao.cursor(dictionary=True) as cursor:
                if parametros:
                    cursor.execute(query, parametros)
                else:
                    cursor.execute(query)
                resultados = cursor.fetchall()
                return resultados
        except Error as e:
            print(f"Erro ao buscar dados: {e}")
            return []


