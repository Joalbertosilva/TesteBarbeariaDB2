import pyodbc

dados_conexao = (
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-E5PU5HI;"
    "DATABASE=Barbearia;"
)
conexao = pyodbc.connect(dados_conexao)
print()
print('Conexão realizada!')

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
usuario_horario()
