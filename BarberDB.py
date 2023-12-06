from principal import cadastro, login, marcar, remarcar
from main import usuario_agenda, delete_condicao, delete, tabela, delete_usuario
from random import randint
import getpass
import pyodbc
def cadastro_user():
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
    print()
    cadastro(idUsuario, email, senha, nome)

def login_user():
    email = input('Digite seu e-mail ou nome de usuário: ')
    senha = getpass.getpass(prompt='Digite sua senha: ')
    print()
    # Verificar se o email e senha correspondem a um usuário registrado
    if login(email, senha):
        marcar_corte()
    else:
        print('Login inválido. Tente novamente.')

def marcar_corte():
    dados_conexao = (
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-E5PU5HI;"
        "DATABASE=Barbearia;"
        )
    conexao = pyodbc.connect(dados_conexao)
    cursor = conexao.cursor()
    print('Acesso liberado!')
    print()
    idUsuario = int(input('''
Insira seu id usuario para poder acumular pontos no nosso salão.
Quando você atingir a meta de 3 cortes em sequência, receberá um corte grátis: '''))

    nome = input('Digite seu nome: ')

    # Aqui você pode obter o horário e dia escolhidos pelo cliente
    print(f'Muito bem {nome}, agora escolha o serviço e a data!')
    print()
    corte = input('''\nEsolha um dos serviços abaixo: 
            1. Cabelo, corte normal: R$15
            2. Cabelo + sobrancelha: R$20
            3. Cabelo + Barba: R$30
            4. Cabelo + Sobrancelha + Barba: R$35
            5. Sobrancelha: R$7 
            6. Barba: R$15
            7. Barbaterapia + Corte: R$50
            8. Platinar + Corte: R$100
            : ''') 
    print()
    cursor.execute("SELECT dia, horario FROM horario")
    horas = cursor.fetchall()
    print("Horários indisponíveis:")
    for hora in horas:
        dia, horario = hora  # Desempacotando os valores retornados
        print(f"|{dia} - {horario}|")

        print()
    data = input('''Escolha o dia.
            1 - Segunda-Feira
            2 - Terça-Feira
            3 - Quarta-Feira
            4 - Quinta-Feira
            5 - Sexta-Feira
            6 - Sábado
            : ''')
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
    marcar(idUsuario, nome, data, horario, corte)
    
def remarcar_corte():
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
    usuario = int(input('Insira o seu idUsuario: '))
    cursor.execute(f"SELECT TOP 1 idAgenda FROM agenda WHERE idUsuario = {usuario} ORDER BY idAgenda DESC")
    ultimo_id_agenda = cursor.fetchone()

    if ultimo_id_agenda:
    # Último idAgenda encontrado para o usuário
        id_agenda = ultimo_id_agenda[0]
        print(f"Seu último id de agenda é: {id_agenda}")
        print()
        novo_nome = input('Digite seu nome: ')
        print("Horários indisponíveis:\n")
        for hora in horas:
            dia, horario = hora  # Desempacotando os valores retornados
            print(f"|{dia} - {horario}|")
        data = input('''Escolha o dia.
        1 - Segunda-Feira
        2 - Terça-Feira
        3 - Quarta-Feira
        4 - Quinta-Feira
        5 - Sexta-Feira
        6 - Sábado
        : ''')
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
        id_agenda = input('Digite o ID da agenda a ser remarcada: ')
        remarcar(novo_nome, data, horario, id_agenda)
    else: 
        print('Usuario não encontrado!')

def menu():
    while True:
        try:
            menu_opcao = int(input('''
            Escolha uma opção:      
            1. Cadastro
            2. Login
            3. Remarcar
            4. Mostrar agenda 
            5. Mostrar tabelas            
            6. Deletar dados específicos
            7. Deletar toda tabela
            8. Deletar usuario
            9. Sair
            : '''))

            if menu_opcao == 1:
                cadastro_user()
            elif menu_opcao == 2:
                login_user()
            elif menu_opcao == 3:
                remarcar_corte()
            elif menu_opcao == 4:
                usuario_agenda()
            elif menu_opcao == 5:
                tabela()
            elif menu_opcao == 6:
                delete_condicao()
            elif menu_opcao == 7:
                delete()
            elif menu_opcao == 8:
                delete_usuario()
            elif menu_opcao == 9:
                print("Programa encerrado. Volte sempre!")
            else:
                print('Opção inválida.') 
                
        except ValueError:
            print("Por favor, insira um número inteiro válido.")
            print()

menu()