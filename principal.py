import pyodbc
from random import randint
import getpass

dados_conexao = (
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-E5PU5HI;"
    "DATABASE=Barbearia;"
)
conexao = pyodbc.connect(dados_conexao)
print()
print('Conexão realizada!')

cursor = conexao.cursor()
def cadastro():    
    dados_conexao = (
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-E5PU5HI;"
    "DATABASE=Barbearia;"
    )
    conexao = pyodbc.connect(dados_conexao)
    cursor = conexao.cursor()
    idUsers = []
    idUsuario = randint(1, 1000)
    idUsers.append(idUsuario)
    while idUsuario == idUsers:
        idUsuario = randint(1, 1000)
    idUsers.append(idUsuario)
    print()
    email = input('Digite seu e-mail ou nome de usuário: ')
    senha = getpass.getpass(prompt='Crie sua senha: ')
    nome = input('Insira seu nome: ')

    # Executar a consulta para verificar se o usuário já existe
    cursor.execute(f"SELECT * FROM usuario WHERE email = '{email}'")
    usuario = cursor.fetchone()

    if not usuario:
        # Se não houver um usuário com o email fornecido, realizar o cadastro
        cursor.execute(f"""INSERT INTO usuario (idUsuario, email, senha, nome) 
                        VALUES ({idUsuario}, '{email}', '{senha}', '{nome}')""")
        conexao.commit()
        print('Cadastro realizado com sucesso!')
    else:
        print('Nome de usuário já utilizado ou email inválido, tente novamente.')

def login():
    # Conectar ao banco de dados
    dados_conexao = (
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-E5PU5HI;"
    "DATABASE=Barbearia;"
    )
    conexao = pyodbc.connect(dados_conexao)
    cursor = conexao.cursor()

    email = input('Digite seu e-mail ou nome de usuário: ')
    senha = getpass.getpass(prompt='Digite sua senha: ')
    # Verificar se o email e senha correspondem a um usuário registrado
    cursor.execute(f"SELECT * FROM usuario WHERE email = '{email}' AND senha = '{senha}'")
    usuario = cursor.fetchone()

    if usuario:
        print('Login bem-sucedido!')
        print()
        marcar()
        # Aqui você pode adicionar qualquer lógica adicional que deseja executar após o login ser bem-sucedido
    else:
        print('E-mail ou senha incorretos. Tente novamente.')
        login()
    conexao.close()
    print()

def marcar():
    dados_conexao = (
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-E5PU5HI;"
    "DATABASE=Barbearia;"
    )
    conexao = pyodbc.connect(dados_conexao)
    cursor = conexao.cursor()
    idUsuario = int(input('''
    Insira seu id usuario para poder acumular pontos no nosso salão.
    Quando você atingir a meta de 3 cortes em sequência, receberá um desconto: '''))
    cursor.execute(f"SELECT * FROM usuario where idUsuario = {idUsuario}")
    verificando = cursor.fetchall()

    if verificando:
        agenda = []
        idAgenda = randint(1, 1000)
        agenda.append(idAgenda)
        while idAgenda == agenda:
            idAgenda = randint(1, 1000)
        agenda.append(idAgenda)
        print()
        nome = input('Digite seu nome: ')
        print(f'Muito bem {nome}, agora escolha o horário!')
        print()

        cursor.execute("SELECT dia, horario FROM horario")
        horas = cursor.fetchall()

        print("Horários indisponíveis:")
        for hora in horas:
            dia, horario = hora  # Desempacotando os valores retornados
            print(f"{dia} - {horario}\n")

        print()

        dias = {
        '1': 'Segunda-Feira',
        '2': 'Terça-Feira',
        '3': 'Quarta-Feira',
        '4': 'Quinta-Feira',
        '5': 'Sexta-Feira',
        '6': 'Sábado',
    }

        data = input('''Escolha o dia.
        1 - Segunda-Feira
        2 - Terça-Feira
        3 - Quarta-Feira
        4 - Quinta-Feira
        5 - Sexta-Feira
        6 - Sábado
        : ''')

        if data in dias:
            dia_escolhido = dias[data]
        else:
            print('Opção de dia inválida.')
    # Aqui você pode decidir se deseja sair do programa ou lidar com o erro de outra forma
            exit()

        horarios = {
            '1': '08:00',
            '2': '09:00',
            '3': '10:00',
            '4': '11:00',
            '5': '12:00',
            '6': '14:00',
            '7': '15:00',
        }

        print()
        horario = input('''Escolha o horário
        1 - 08:00
        2 - 09:00
        3 - 10:00
        4 - 11:00
        5 - 12:00
        6 - 14:00
        7 - 15:00
        : ''')

        if horario in horarios:
            horario_escolhido = horarios[horario]
        else:
            print('Opção de horário inválida.')
    # Aqui você pode decidir se deseja sair do programa ou lidar com o erro de outra forma
        cursor.execute(f"SELECT * FROM agenda WHERE horario = '{horario_escolhido}' AND dia = '{dia_escolhido}'")
        agenda = cursor.fetchone()
        corte = 'cabelo'

        if not agenda:
            cursor.execute(f"""INSERT INTO agenda (idAgenda, nome, horario, dia, idUsuario, corte) VALUES ({idAgenda}, '{nome}', '{horario_escolhido}', '{dia_escolhido}', {idUsuario}, '{corte}')""")
            conexao.commit()
            print(f'Muito bem {nome}, processo finalizado. O seu número da agenda é {idAgenda}, guarde-o caso precise remarcar.')
            print('Horário marcado com sucesso, esperamos por você!')
            cursor.execute(f"""INSERT INTO horario (dia, horario, idAgenda) VALUES ('{dia_escolhido}', '{horario_escolhido}', {idAgenda})""")
            conexao.commit()
            cursor.execute(f"SELECT COUNT(*) FROM agenda WHERE idUsuario = {idUsuario}")
            quantidade_cortes = cursor.fetchone()[0]

            if quantidade_cortes == 3:
                print('Parabéns! Você ganhou um desconto de 5% no próximo corte!')
            # Aqui você pode aplicar o desconto ao próximo corte para o usuário
            # Por exemplo, atualizar um campo na tabela de usuários para marcar o desconto
            # ou aplicar diretamente na lógica de pagamento

            if quantidade_cortes > 3:
                cursor.execute(f"UPDATE agenda SET corte = 0 WHERE idUsuario = {idUsuario}")
                conexao.commit()
       
        else:
            print('Horário indisponível. Tente novamente.')
    # Se desejar, pode chamar a função marcar() para tentar novamente
            marcar()
            print()
        cursor.execute(f"SELECT * FROM agenda WHERE idUsuario = {idAgenda}")
        agenda = cursor.fetchone()
    else:
        print()
        print('IdUsuario inexistente. Tente novamente. ')

def remarcar():
    dados_conexao = (
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-E5PU5HI;"
        "DATABASE=Barbearia;"
    )
    conexao = pyodbc.connect(dados_conexao)
    cursor = conexao.cursor()
    cursor.execute("SELECT dia, horario FROM horario")
    horas = cursor.fetchall()

    # Se a agenda existe, atualize os dados
    novo_nome = input('Digite seu nome: ')
    print("Horários indisponíveis:")
    for hora in horas:
        dia, horario = hora  # Desempacotando os valores retornados
        print(f"{dia} - {horario}\n")

        print()

    dias = {
        '1': 'Segunda-Feira',
        '2': 'Terça-Feira',
        '3': 'Quarta-Feira',
        '4': 'Quinta-Feira',
        '5': 'Sexta-Feira',
        '6': 'Sábado',
        }
    data = input('''Escolha o dia.
    1 - Segunda-Feira
    2 - Terça-Feira
    3 - Quarta-Feira
    4 - Quinta-Feira
    5 - Sexta-Feira
    6 - Sábado
    : ''')
    if data in dias:
        novo_dia = dias[data]
    else:
        print('Opção de dia inválida. Escolha novamente')
        remarcar()
        return

    print()
    horarios = {
        '1': '08:00',
        '2': '09:00',
        '3': '10:00',
        '4': '11:00',
        '5': '12:00',
        '6': '13:00',
        '7': '14:00',
        }
    horario = input('''Escolha o horário
    1 - 08:00
    2 - 09:00
    3 - 10:00
    4 - 11:00
    5 - 12:00
    6 - 14:00
    7 - 15:00   
    : ''')
    if horario in horarios:
        novo_horario = horarios[horario]
    else:
        print('Opção de horário inválida.')
        return

    id_agenda = input('Digite o ID da agenda a ser remarcada: ')

    cursor.execute("SELECT * FROM agenda WHERE idAgenda = ?", id_agenda)
    agenda_existente = cursor.fetchone()
    if agenda_existente:
        try:
            cursor.execute("UPDATE agenda SET nome = ?, horario = ?, dia = ? WHERE idAgenda = ?", (novo_nome, novo_horario, novo_dia, id_agenda))
            conexao.commit()
            print('Agenda remarcada com sucesso no banco de dados!')

        # Atualização na tabela 'horario'
            cursor.execute("UPDATE horario SET dia = ?, horario = ? WHERE idAgenda = ?", (novo_dia, novo_horario, id_agenda))
            conexao.commit()
        except pyodbc.Error as ex:
            print('Não foi possível remarcar a agenda. Tente novamente.', ex)
    else:
        print('Agenda não encontrada.')
       

    # Atualizar o arquivo de texto com a nova informação

        conexao.close()

while True:
    menu = int(input('''
    Escolha uma opção      
    1. Cadastro
    2. Login
    3. Remarcar
    4. Sair
    : '''))

    if menu == 1:
        cadastro()
    elif menu == 2:
        login()
    elif menu == 3:
        remarcar()
    elif menu == 4:
        break;
    elif menu >= 5:
        print('Opção inválida.') 



#adicionar dois atributos e agenda, o id do usuario e o corte escolhido. 
#idUsuario foreign key + corte varchar
#fazer o programa ler a quantidade de cortes do cliente, quando ele chegar em 3 ele ganha um desconto de 5%. 
#Após isso ele apaga do sistema pra sempre ficar na contagem até 3
#criar uma tabela para realizar um desconto. la ele vai receber o seu id e toda vez ele vai inserir, assim vai realizar a leitura
#receber um idusuario para armazenar a quantidade de cortes e dar o desconto se esse id tiver na tabela num total de 3 vezes