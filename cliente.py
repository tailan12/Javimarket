import sqlite3

def cadastrar_usuario(conn):
    cursor = conn.cursor()
    while True:
        print("\nCadastro de usuário:")
        username = input("Digite um nome de usuário: ")
        senha = input("Digite uma senha: ")
        email = input("Digite seu e-mail: ")
        endereco = input("Digite seu endereço: ")
        cpf = input("Digite seu CPF: ")

        try:
            cursor.execute(
                "INSERT INTO usuarios (username, senha, email, endereco, cpf) VALUES (?, ?, ?, ?, ?)",
                (username, senha, email, endereco, cpf),
            )
            conn.commit()
            print("Usuário cadastrado com sucesso!")
            break
        except sqlite3.IntegrityError:
            print("Nome de usuário ou CPF já existem. Tente novamente.")


def login_usuario(conn):
    cursor = conn.cursor()
    print("\nLogin de usuário:")
    username = input("Digite seu nome de usuário: ")
    senha = input("Digite sua senha: ")
    cursor.execute(
        "SELECT * FROM usuarios WHERE username = ? AND senha = ?",
        (username, senha),
    )
    usuario = cursor.fetchone()
    if usuario:
        print(f"Bem-vindo, {username}!")
        return True
    else:
        print("Nome de usuário ou senha incorretos.")
        return False
