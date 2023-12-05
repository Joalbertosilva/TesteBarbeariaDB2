import pyodbc

dados_conexao = (
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-E5PU5HI;"
    "DATABASE=Barbearia;"
)
conexao = pyodbc.connect(dados_conexao)
print()


cursor = conexao.cursor()


def print_table(rows, headers):
    col_width = [max(len(str(x)) for x in col) for col in zip(*rows, headers)]
    print(' | '.join("{:{}}".format(h, col_width[i]) for i, h in enumerate(headers)))
    print('-' * (sum(col_width) + 3 * len(col_width) - 1))
    for row in rows:
        print(' | '.join("{:{}}".format(r, col_width[i]) for i, r in enumerate(row)))

def usuario_tabela():
    cursor.execute('SELECT * FROM usuario')
    columns = [column[0] for column in cursor.description]
    results = cursor.fetchall()
    print_table(results, columns)

# Fechando conexão com o banco de dados
def agenda_tabela():
    cursor.execute('SELECT * FROM agenda')
    columns = [column[0] for column in cursor.description]
    results = cursor.fetchall()
    print_table(results, columns)

def horario_tabela():
    cursor.execute('SELECT * FROM horario')
    columns = [column[0] for column in cursor.description]
    results = cursor.fetchall()
    print_table(results, columns)

def usuario_horario():
    cursor = conexao.cursor()

    print()
    usuario = int(input('Insira seu id de usuario: '))
    sql_query = '''
    SELECT a.nome, a.horario, a.dia, a.corte
    FROM agenda a
    INNER JOIN horario h ON a.dia = h.dia AND a.horario = h.horario AND h.idUsuario = ?
    WHERE a.idAgenda = (
        SELECT TOP 1 idAgenda
        FROM agenda
        WHERE idUsuario = ?
        ORDER BY idAgenda DESC
    )
'''
# Executando a consulta com parâmetros
    cursor.execute(sql_query, usuario, usuario)

# Obtendo os resultados
    resultado = cursor.fetchone()

# Exibindo o resultado, se existir
    if resultado:
        print(f'Nome: {resultado.nome}, Horário: {resultado.horario}, Dia: {resultado.dia}, Corte: {resultado.corte}')
    else:
        print('Nenhum registro encontrado para este usuário.')

def usuario_agenda():
    cursor = conexao.cursor()
    usuario = input('Insira o id usuario: ')
    sql_query = f"""
    SELECT u.idUsuario, a.nome, a.dia, a.horario
    FROM usuario u
    INNER JOIN agenda a ON u.idUsuario = a.idUsuario
    WHERE u.idUsuario = '{usuario}'
""" 
    cursor.execute(sql_query)
    resultado = cursor.fetchall()
    columns = [column[0] for column in cursor.description]

    # Imprime os nomes das colunas separados por barras com espaços adicionados
    print(f"{columns[0]:^10} | {columns[1]:^20} | {columns[2]:^20} | {columns[3]:^20}")
    print("-" * 70)

    # Imprimir os resultados
    for row in resultado:
        print(f"{row[0]:^10} | {row[1]:^20} | {row[2]:^20} | {row[3]:^20}")


def delete():
    cursor = conexao.cursor()
    tabela = input('Insira tabela para deletar: ')
    try:
        cursor.execute(f"DELETE FROM {tabela}")
        conexao.commit()
        print("Registros excluídos com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao excluir registros: {str(e)}")
    finally:
        cursor.close()
        conexao.close()

def delete_condicao():
    cursor = conexao.cursor()
    tabela = input('Insira tabela para deletar: ')
    condicao = input('Insira condicao para deletar: ')
    try:
        cursor.execute(f"DELETE FROM {tabela} WHERE {condicao}")
        conexao.commit()
        print("Dados excluídos com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao excluir registros: {str(e)}")
    finally:
        cursor.close()
        conexao.close()


