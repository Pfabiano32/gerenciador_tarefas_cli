import typer
from src.gerenciador import GerenciadorTarefas
from src.tarefas import Tarefa, TarefaUrgente  # Adicione "Tarefa" aqui

app = typer.Typer()
gerenciador = GerenciadorTarefas()

@app.command()
def adicionar(
    titulo: str,
    descricao: str = typer.Option(None),
    prioridade: str = typer.Option("media"),
    prazo: str = typer.Option(None),
    urgente: bool = typer.Option(False)
):
    """Adiciona uma nova tarefa"""
    try:
        # Verifica se há conexão antes de adicionar
        if not gerenciador.db.conexao or not gerenciador.db.conexao.is_connected():
            raise Exception("Sem conexão com o banco de dados!")
        
        if urgente:
            tarefa = TarefaUrgente(titulo, descricao, prazo)
        else:
            tarefa = Tarefa(titulo, descricao, prioridade, prazo)
        
        gerenciador.adicionar_tarefa(tarefa)
        
        typer.secho()
        typer.secho(f"Tarefa '{titulo}' adicionada com sucesso!", fg=typer.colors.GREEN)
        typer.secho()
    except Exception as e:
        typer.secho()
        typer.secho(f"🚨 ERRO: {e}", fg=typer.colors.RED, bold=True)
        typer.secho("A tarefa NÃO foi salva.", fg=typer.colors.YELLOW)
        typer.secho()

@app.command()
def listar(filtro_prioridade: str = typer.Option(None)):
    """Lista tarefas com filtro opcional"""
    tarefas = gerenciador.listar_tarefas(filtro_prioridade)

    if not tarefas:
        typer.echo()
        typer.secho("Nenhuma tarefa encontrada.", fg=typer.colors.YELLOW)
        return
    
    for tarefa in tarefas:
        typer.echo()
        status = "Concluída" if tarefa['concluida'] else "Pendente"
        typer.echo(f"ID: {tarefa['id']} - [{tarefa['prioridade'].upper()}] {tarefa['titulo']} (Prazo: {tarefa['prazo']}, Tipo: {tarefa['tipo']}, Status: {status})")
        typer.echo()

@app.command()
def concluir(id: int):
    """Marca uma tarefa como concluída"""
    try:
        # Buscar a tarefa pelo ID para obter o título
        query = "SELECT * FROM tarefas WHERE id = %s"
        resultado = gerenciador.db.buscar_dados(query, (id,))

        if not resultado:
            raise Exception("Tarefa não encontrada!")

        tarefa = resultado[0]

        gerenciador.marcar_concluida(id)

        typer.secho()
        # Exibir a mensagem de confirmação com o título da tarefa
        typer.secho(f"Tarefa '{tarefa['titulo']}' (ID: {id}) marcada como concluída!", fg=typer.colors.GREEN)
        typer.secho()

    except Exception as e:
        typer.secho()
        typer.secho(f"Erro: {e}", fg=typer.colors.RED)
        typer.secho()

@app.command()
def excluir(id: int):
    """Exclui uma tarefa específica (confirma se pendente)"""
    try:
        # Busca a tarefa para verificar status
        tarefa = gerenciador.db.buscar_dados("SELECT * FROM tarefas WHERE id = %s", (id,))
        
        if not tarefa:
            raise Exception("🚨 Tarefa não encontrada!")
        
        tarefa = tarefa[0]
        confirmar = True
        
        if not tarefa['concluida']:
            typer.secho("\n⚠️  ESTA TAREFA ESTÁ PENDENTE!", fg=typer.colors.YELLOW, bold=True)
            
            # Loop até resposta válida
            while True:
                resposta = typer.prompt(
                    "Deseja realmente excluir? (S/N)",
                    default="N",
                    show_default=False
                ).strip().lower()

                if resposta in ["s", "n"]:
                    confirmar = resposta == "s"
                    break
                else:
                    typer.secho()
                    typer.secho("Entrada inválida! Use apenas S (Sim) ou N (Não).", fg=typer.colors.RED)
                    typer.secho()

        if confirmar:
            gerenciador.excluir_tarefa(id)
            typer.secho(f"\n✅ Tarefa ID {id} excluída com sucesso!\n", fg=typer.colors.GREEN)
        else:
            typer.secho("\n❌ Exclusão cancelada.\n", fg=typer.colors.YELLOW)
            
    except Exception as e:
        typer.secho(f"\n🔥 ERRO CRÍTICO: {e}\n", fg=typer.colors.RED, bold=True)

@app.command()
def limpar_concluidas():
    """Exclui todas as tarefas concluídas"""
    try:
        total = gerenciador.excluir_tarefas_concluidas()
        if total > 0:
            typer.secho()
            typer.secho(f"🗑️  {total} tarefas concluídas excluídas!", fg=typer.colors.GREEN)
        else:
            typer.secho()
            typer.secho("ℹ️  Nenhuma tarefa concluída para excluir.", fg=typer.colors.BLUE)
    except Exception as e:
        typer.secho(f"🚨 ERRO: {e}", fg=typer.colors.RED)

if __name__ == "__main__":
    gerenciador.inicializar()  # Chama a inicialização UMA vez
    app()