import sqlite3
from util import listar_produtos

def adicionar_novo_produto(cursor, conn):
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

def editar_produto(cursor, conn):
    listar_produtos(cursor)
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

def remover_produto(cursor, conn):
    listar_produtos(cursor)
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
