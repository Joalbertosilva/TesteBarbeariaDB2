from principal import cadastro, login, marcar, remarcar
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
    cadastro(idUsuario, email, senha, nome)

def login_user():
    email = input('Digite seu e-mail ou nome de usuário: ')
    senha = getpass.getpass(prompt='Digite sua senha: ')
    # Verificar se o email e senha correspondem a um usuário registrado
    if login(email, senha):
        marcar_corte()
    else:
        print('Login inválido. Tente novamente.')

def marcar_corte():
    idUsuario = int(input('''
    Insira seu id usuario para poder acumular pontos no nosso salão.
    Quando você atingir a meta de 3 cortes em sequência, receberá um desconto: '''))
    marcar(idUsuario)

def remarcar():
    print
while True:
    menu = int(input('''
    Escolha uma opção      
    1. Cadastro
    2. Login
    3. Remarcar
    4. Sair
    : '''))

    if menu == 1:
        cadastro_user()
    elif menu == 2:
        login_user()
    elif menu == 3:
        remarcar()
    elif menu == 4:
        break;
    elif menu >= 5:
        print('Opção inválida.') 

