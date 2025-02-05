def cadastrar_usuario(cursor, conn):
    while True:
        print("\nCadastro de usuário:")
        username = input("Digite um nome de usuário: ")
        senha = input("Digite uma senha: ")
        try:
            cursor.execute(
                "INSERT INTO usuarios (username, senha) VALUES (?, ?)",
                (username, senha),
            )
            conn.commit()
            print("Usuário cadastrado com sucesso!")
            break
        except sqlite3.IntegrityError:
            print("Nome de usuário já existe. Tente outro.")

def login_usuario(cursor):
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
