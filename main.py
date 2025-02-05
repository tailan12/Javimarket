import sqlite3



conn = sqlite3.connect("feira.db")
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
    senha TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS supermercados(
    id INTEGER PRIMARY KEY,
nome TEXT UNIQUE NOT NULL
)
''')

def adicionar_supermercado():
    print("\nCadastro de novo supermercado:")
    nome_supermercado = input("digite o nome do supermercado: ")
    cursor.execute(
    "INSERT INTO supermercados (nome) VALUES (?)",
    (nome_supermercado,)
    )
    conn.commit()
    print(f"supermercado '{nome_supermercado}' cadastrado com sucesso!")


def cadastrar_usuario():
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

def login_usuario():
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

def listar_produtos():
    print("\nProdutos disponíveis:")
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    if produtos:
        for row in produtos:
            print(f"ID: {row[0]} | Nome: {row[1]} | Atacadão: R${row[2]:.2f} | Açaí: R${row[3]:.2f}")
    else:
        print("Nenhum produto disponível.")

def adicionar_novo_produto():
    while True:
        print("\nAdicionando novo produto:")
        nome = input("Digite o nome do produto: ")
        try:
            preco_atacadao = float(input("Digite o preço no Atacadão: R$"))
            preco_acai = float(input("Digite o preço no Açaí: R$"))
            cursor.execute(
                "INSERT INTO produtos (nome, preco_atacadao, preco_acai) VALUES (?, ?, ?)",
                (nome, preco_atacadao, preco_acai),
            )
            conn.commit()
            print(f"Produto '{nome}' adicionado com sucesso!")
        except ValueError:
            print("Preço inválido. Tente novamente.")
        opcao = input("Deseja adicionar outro produto? (s/n): ").lower()
        if opcao != "s":
            break

def editar_produto():
    listar_produtos()
    try:
        produto_id = int(input("\nDigite o ID do produto que deseja editar: "))
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
        produto = cursor.fetchone()
        if produto:
            print(f"Editando o produto: {produto[1]}")
            novo_nome = input("Novo nome (deixe em branco para manter): ") or produto[1]
            novo_preco_atacadao = input(f"Novo preço Atacadão (atual: R${produto[2]:.2f}): ") or produto[2]
            novo_preco_acai = input(f"Novo preço Açaí (atual: R${produto[3]:.2f}): ") or produto[3]
            cursor.execute(
                "UPDATE produtos SET nome = ?, preco_atacadao = ?, preco_acai = ? WHERE id = ?",
                (novo_nome, float(novo_preco_atacadao), float(novo_preco_acai), produto_id),
            )
            conn.commit()
            print("Produto atualizado com sucesso!")
        else:
            print("Produto não encontrado.")
    except ValueError:
        print("Entrada inválida. Tente novamente.")

def remover_produto():
    listar_produtos()
    try:
        produto_id = int(input("\nDigite o ID do produto que deseja remover: "))
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
        produto = cursor.fetchone()
        if produto:
            cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
            conn.commit()
            print(f"Produto '{produto[1]}' removido com sucesso!")
        else:
            print("Produto não encontrado.")
    except ValueError:
        print("Entrada inválida. Tente novamente.")

def adicionar_ao_carrinho(carrinho, produto_id, quantidade):
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
    produto = cursor.fetchone()
    if produto:
        carrinho.append({"produto": produto, "quantidade": quantidade})
        print(f"Adicionado: {produto[1]} (x{quantidade})")
    else:
        print("Produto não encontrado.")

def calcular_total(carrinho):
    total_atacadao = sum(item["produto"][2] * item["quantidade"] for item in carrinho)
    total_acai = sum(item["produto"][3] * item["quantidade"] for item in carrinho)
    return total_atacadao, total_acai

def menu_administrador():
    while True:
        print("\nMenu do Administrador:")
        print("1. Adicionar produtos")
        print("2. Editar produtos")
        print("3. Remover produtos")
        print("4. Listar produtos")
        print("5. Voltar")
        print("6. adicionar supermercado")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_novo_produto()
        elif opcao == "2":
            editar_produto()
        elif opcao == "3":
            remover_produto()
        elif opcao == "4":
            listar_produtos()
        elif opcao == "5":
            break
        elif opcao == "6":
            adicionar_supermercado()
        else:
            print("Opção inválida. Tente novamente.")

def menu_usuario():
    carrinho = []
    while True:
        listar_produtos()
        opcao = input("\nDigite o ID do produto para adicionar ao carrinho (ou 'finalizar' para encerrar): ")
        if opcao.lower() == "finalizar":
            break
        try:
            produto_id = int(opcao)
            quantidade = int(input("Digite a quantidade: "))
            adicionar_ao_carrinho(carrinho, produto_id, quantidade)
        except ValueError:
            print("Entrada inválida. Tente novamente.")

    total_atacadao, total_acai = calcular_total(carrinho)
    print(f"\nTotal Atacadão: R${total_atacadao:.2f}")
    print(f"Total Açaí: R${total_acai:.2f}")

    loja_mais_barata = "Atacadão" if total_atacadao < total_acai else "Açaí"
    print(f"Loja mais barata: {loja_mais_barata}")

    escolha_entrega = input("Deseja adicionar entrega por R$10.00? (s/n): ").lower()
    custo_entrega = 10.00 if escolha_entrega == "s" else 0.00

    total_final = (total_atacadao if loja_mais_barata == "Atacadão" else total_acai) + custo_entrega
    print(f"\nTotal final com entrega: R${total_final:.2f}")

def main():
    while True:
        print("\nEscolha seu perfil:")
        print("1. Administrador")
        print("2. Usuário")
        print("3. Cadastrar usuário")
        print("4. Login")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_administrador()
        elif opcao == "2":
            menu_usuario()
        elif opcao == "3":
            cadastrar_usuario()
        elif opcao == "4":
            login_usuario()
        elif opcao == "5":
            print("Encerrando o programa. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()

conn.close()

