import sqlite3

def conectar_banco(db_name="feira.db"):
    """Retorna uma conexão com o banco de dados."""
    return sqlite3.connect(db_name)

def criar_tabelas(conn):
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        preco_atacadao REAL NOT NULL,
        preco_acai REAL NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        endereco TEXT NOT NULL,
        cpf TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS supermercados (
        id INTEGER PRIMARY KEY,
        nome TEXT UNIQUE NOT NULL
    )
    ''')

    conn.commit()


def adicionar_supermercado(conn):
    """Cadastra um novo supermercado na tabela."""
    print("\nCadastro de novo supermercado:")
    nome_supermercado = input("Digite o nome do supermercado: ")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO supermercados (nome) VALUES (?)",
        (nome_supermercado,)
    )
    conn.commit()
    print(f"Supermercado '{nome_supermercado}' cadastrado com sucesso!")
