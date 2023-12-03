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
def cadastro(idUsuario, email, senha, nome):    
    dados_conexao = (
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-E5PU5HI;"
    "DATABASE=Barbearia;"
    )
    conexao = pyodbc.connect(dados_conexao)
    cursor = conexao.cursor()

    # Executar a consulta para verificar se o usuário já existe
    cursor.execute(f"SELECT * FROM usuario WHERE email = '{email}'")
    usuario = cursor.fetchone()

    if not usuario:
        # Se não houver um usuário com o email fornecido, realizar o cadastro
        cursor.execute(f"""INSERT INTO usuario (idUsuario, email, senha, nome) 
                        VALUES ({idUsuario}, '{email}', '{senha}', '{nome}')""")
        conexao.commit()
        print('Cadastro realizado com sucesso!')
        print(f"Seu id de usuario é: {idUsuario}")
    else:
        print('Nome de usuário já utilizado ou email inválido, tente novamente.')

def login(email, senha):
    try:
        dados_conexao = (
            "DRIVER={SQL Server};"
            "SERVER=DESKTOP-E5PU5HI;"
            "DATABASE=Barbearia;"
        )
        conexao = pyodbc.connect(dados_conexao)
        cursor = conexao.cursor()

        # Verificar se o email e senha correspondem a um usuário registrado
        cursor.execute(f"SELECT * FROM usuario WHERE email = '{email}' AND senha = '{senha}'")
        usuario = cursor.fetchone()

        conexao.close()

        return usuario is not None  # Retorna True se o usuário existe, senão retorna False
    except Exception as e:
        print(f"Ocorreu um erro ao tentar fazer login: {str(e)}")
        return False

def marcar(idUsuario, nome, data, horario, corte):
    try:
        dados_conexao = (
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-E5PU5HI;"
        "DATABASE=Barbearia;"
        )
        conexao = pyodbc.connect(dados_conexao)
        cursor = conexao.cursor()
        cursor.execute(f"SELECT * FROM usuario where idUsuario = {idUsuario}")
        
        agenda = []
        idAgenda = randint(1, 1000)
        agenda.append(idAgenda)
        while idAgenda == agenda:
            idAgenda = randint(1, 1000)
        agenda.append(idAgenda)
            
        print()
        servicos = {
            '1': 'Cabelo',
            '2': 'Cabelo + Sobrancelha',
            '3': 'Cabelo + barba',
            '4': 'Cabelo + Sobrancelha + Barba',
            '5': 'Sobrancelha',
            '6': 'Barba',
            '7': 'Barbaterapia + corte',
            '8': 'Platinar'
            }
        if corte in servicos:
            corte_escolhido = servicos[corte]
        try:
            corte_escolhido = servicos[corte]
        except KeyError:
            print("Opção de escolha não foi validada. Encontramos um erro na sua escolha, tente marcar novamente e respeite os numeros apresentados.")
            return False
        dias = {
            '1': 'Segunda-Feira',
            '2': 'Terça-Feira',
            '3': 'Quarta-Feira',
            '4': 'Quinta-Feira',
            '5': 'Sexta-Feira',
            '6': 'Sábado',
        }
        if data in dias:
            dia_escolhido = dias[data]
        try:
            dia_escolhido = dias[data]
        except KeyError:
            print("Opção de escolha não foi validada. Encontramos um erro na sua escolha, tente marcar novamente e respeite os numeros apresentados.")
            return False

        horarios = {
                '1': '08:00',
                '2': '09:00',
                '3': '10:00',
                '4': '11:00',
                '5': '12:00',
                '6': '14:00',
                '7': '15:00',
            }

        if horario in horarios:
            horario_escolhido = horarios[horario]
        try:
            horario_escolhido = horarios[horario]
        except KeyError:
            print("Opção de escolha não foi validada. Encontramos um erro na sua escolha, tente marcar novamente e respeite os numeros apresentados.")
            return False
        # Aqui você pode decidir se deseja sair do programa ou lidar com o erro de outra forma
        cursor.execute(f"SELECT * FROM agenda WHERE horario = '{horario_escolhido}' AND dia = '{dia_escolhido}'")
        agenda = cursor.fetchone()

        if not agenda:
            cursor.execute(f"""INSERT INTO agenda (idAgenda, nome, horario, dia, idUsuario, corte) VALUES ({idAgenda}, '{nome}', '{horario_escolhido}', '{dia_escolhido}', {idUsuario}, '{corte_escolhido}')""")
            conexao.commit()
            print(f'Muito bem {nome}, processo finalizado. O seu número da agenda é {idAgenda}, guarde-o caso precise remarcar.')
            print('Horário marcado com sucesso, esperamos por você!')
            cursor.execute(f"""INSERT INTO horario (dia, horario, idAgenda, idUsuario) VALUES ('{dia_escolhido}', '{horario_escolhido}', {idAgenda}, {idUsuario})""")
            conexao.commit()
            cursor.execute(f"SELECT COUNT(*) FROM agenda WHERE idUsuario = {idUsuario}")
            quantidade_cortes = cursor.fetchone()[0]

            if quantidade_cortes % 3 == 0:
                print('Parabéns! Você ganhou um desconto de 5% no próximo corte!')
                # Aqui você pode aplicar o desconto ao próximo corte para o usuário
                # Por exemplo, atualizar um campo na tabela de usuários para marcar o desconto
                # ou aplicar diretamente na lógica de pagamento
        else:
            print('Horário insdisponível. Tente novamente.')
        # Se desejar, pode chamar a função marcar() para tentar novamente
            print()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar fazer login: {str(e)}")
        return False
def remarcar(novo_nome, data, horario, id_agenda):
    dados_conexao = (
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-E5PU5HI;"
        "DATABASE=Barbearia;"
    )
    conexao = pyodbc.connect(dados_conexao)
    cursor = conexao.cursor()
    cursor.execute("SELECT dia, horario FROM horario")

    dias = {
        '1': 'Segunda-Feira',
        '2': 'Terça-Feira',
        '3': 'Quarta-Feira',
        '4': 'Quinta-Feira',
        '5': 'Sexta-Feira',
        '6': 'Sábado',
        }
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
    if horario in horarios:
        novo_horario = horarios[horario]
    else:
        print('Opção de horário inválida.')
        return

    cursor.execute("SELECT * FROM agenda WHERE idAgenda = ?", id_agenda,)
    agenda_existente = cursor.fetchone()
    if agenda_existente:
        try:
            cursor.execute("UPDATE agenda SET nome = ?, horario = ?, dia = ? WHERE idAgenda = ?", (novo_nome, novo_horario, novo_dia, id_agenda,))
            conexao.commit()
            print('Agenda remarcada com sucesso!')

        # Atualização na tabela 'horario'
            cursor.execute("UPDATE horario SET dia = ?, horario = ? WHERE idAgenda = ?", (novo_dia, novo_horario, id_agenda,))
            conexao.commit()
        except pyodbc.Error as ex:
            print('Não foi possível remarcar a agenda. Tente novamente.', ex)
    else:
        print('Agenda não encontrada.')
       

    # Atualizar o arquivo de texto com a nova informação

        conexao.close()



#adicionar dois atributos e agenda, o id do usuario e o corte escolhido. 
#idUsuario foreign key + corte varchar
#fazer o programa ler a quantidade de cortes do cliente, quando ele chegar em 3 ele ganha um desconto de 5%. 
#Após isso ele apaga do sistema pra sempre ficar na contagem até 3
#criar uma tabela para realizar um desconto. la ele vai receber o seu id e toda vez ele vai inserir, assim vai realizar a leitura
#receber um idusuario para armazenar a quantidade de cortes e dar o desconto se esse id tiver na tabela num total de 3 vezes