# Gerenciador de Tarefas em Python + MySQL 📝

Este é um projeto de linha de comando (CLI) feito em Python para gerenciar tarefas com prioridade, prazo e status de conclusão. As tarefas são armazenadas em um banco de dados MySQL que roda em um container Docker.

## Funcionalidades

- ✅ **Adicionar tarefas**: Título, descrição, prioridade (alta/média/baixa), prazo.

- 📋 **Listar tarefas**: Filtro por prioridade ou status (concluídas/pendentes).

- ✔️ **Marcar como concluída**: Por ID da tarefa.

- 🗑️ **Excluir tarefas**:  
  - **Individual**: Confirmação para tarefas pendentes.  
  - **Em massa**: Remove todas as concluídas automaticamente.  

- 🐳 **Banco de dados MySQL**: Container Docker isolado e persistente.

## Pré-requisitos

- Python 3.10+

- Docker + Docker Compose ([Instalação](https://docs.docker.com/get-docker/))

- Bibliotecas Python (`requirements.txt`):

    ````bash
  pip install typer mysql-connector-python python-dotenv
    ````

### ⚠️ Aviso de Segurança:  

> - **Nunca** compartilhe arquivos `.env` ou `docker-compose.yml` com dados reais.

> - Use sempre credenciais fictícias em exemplos públicos.

## Instalação

1. Clone o repositório:
    ```bash
   git clone https://github.com/Pfabiano32/gerenciador_tarefas_cli.git

   cd gerenciador_tarefas_cli
    ```

2. Crie e ative o ambiente virtual:

    ```bash
    python -m venv venv
 
    source venv/bin/activate  # ou venv\Scripts\activate no Windows
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```
**Nota:** Se estiver no Windows, use python -m pip install


## Configuração do Banco de Dados  

1. Renomeie `docker-compose.EXEMPLO.yml` para `docker-compose.yml`  

2. Configure o .env com as mesmas credenciais usadas no Docker:

    ``` bash
    DB_HOST=localhost  # Se o app rodar FORA do Docker
    # ou
    DB_HOST=mysql_db   # Se o app rodar DENTRO do Docker (como outro serviço)
    DB_USER=seu_usuario
    DB_PASSWORD=sua_senha
    DB_NAME=nome_do_banco
    ```

3. Altere as senhas e nomes no arquivo  

4. Inicie o container:

```bash
docker-compose up -d
````

💡 Certifique-se de que as credenciais e o nome do banco de dados no .env sejam os mesmos usados no container docker.

## COMO USAR

Exemplos Detalhados

1. Adicionar Tarefa

    ``` bash
    python main.py adicionar "Corrigir bug crítico" \
      --descricao "Erro na API de pagamentos" \
      --prioridade alta \
      --prazo 2024-05-25 \
      --urgente
    ```

Saída:

  ``` bash
  ✅ Tarefa 'Corrigir bug crítico' adicionada com sucesso!
  ```
2. Listar todas as tarefas

    ``` bash
    python main.py listar
    ```

3. Listar Tarefas por status ou por prioridade

    ``` bash
    python main.py listar --filtro-prioridade alta --status pendentes
    ```

Saída exemplo:

``` bash
ID: 2 - [ALTA] Corrigir bug crítico (Prazo: 2024-05-25, Tipo: urgente, Status: Pendente)
```

4. Marcar tarefas como concluídas

    ``` bash
    python main.py concluir 2 # Marca a tarefa com ID 2 como concluída
    ```

- Observação: O ID da tarefa e mostrado quando é listada.

5. Excluir Tarefa Pendente (Confirmação)

    ``` bash
    python main.py excluir 3
    ```

Saída:

``` bash
⚠️  ESTA TAREFA ESTÁ PENDENTE!  
Deseja realmente excluir? [S/N]: s  

✅ Tarefa ID 2 excluída com sucesso!
```

- Observação: a mensagem de confirmação aparece somente quando for para excluir uma tarefa com status pendente, exclui inserindo o ID da tarefa seguido do comando excluir.

6. Excluir Tarefas concluídas

    ``` bash
    python main.py excluir 3 # tarefa com status concluído
    ```

Saída:

``` bash
🗑️  3 tarefas com palavras 'teste,rascunho' excluídas!
```

- Excluir todas as tarefas com status concluída

    ``` bash
    python main.py limpar-concluidas
    ```

Saída:

``` bash
🗑️  3 tarefas concluídas excluídas!
```

## Estrutura do Projeto


├── main.py

├── requirements.txt

├── README.md

├── env.EXEMPLO

├── docker-compose.EXEMPLO.yml

├── src/

│   ├── __init__.py

│   ├── database.py

│   ├── gerenciador.py

│   └── tarefas.py


## 👨‍💻 Desenvolvido por [Gabriel](https://github.com/Pfabiano32) com 💻 e ☕
