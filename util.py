def conectar_banco():
    conn = sqlite3.connect("feira.db")
    cursor = conn.cursor()
    return conn, cursor

def criar_tabelas(cursor, conn):
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
        senha TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS supermercados(
        id INTEGER PRIMARY KEY,
        nome TEXT UNIQUE NOT NULL
    )
    ''')
    conn.commit()

def listar_produtos(cursor):
    print("\nProdutos disponíveis:")
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    if produtos:
        for row in produtos:
            print(f"ID: {row[0]} | Nome: {row[1]} | Atacadão: R${row[2]:.2f} | Açaí: R${row[3]:.2f}")
    else:
        print("Nenhum produto disponível.")
