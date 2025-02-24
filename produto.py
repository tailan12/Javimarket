


def listar_produtos(conn):
    cursor = conn.cursor()
    print("\nProdutos disponíveis:")
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    if produtos:
        for row in produtos:
            print(
                f"ID: {row[0]} | "
                f"Nome: {row[1]} | "
                f"Atacadão: R${row[2]:.2f} | "
                f"Açaí: R${row[3]:.2f}"
            )
    else:
        print("Nenhum produto disponível.")

def adicionar_novo_produto(conn):
    while True:
        print("\nAdicionando novo produto:")
        nome = input("Digite o nome do produto: ")
        try:
            preco_atacadao = float(input("Digite o preço no Atacadão: R$"))
            preco_acai = float(input("Digite o preço no Açaí: R$"))
            cursor = conn.cursor()
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

def editar_produto(conn):
    listar_produtos(conn)
    cursor = conn.cursor()
    try:
        produto_id = int(input("\nDigite o ID do produto que deseja editar: "))
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
        produto = cursor.fetchone()
        if produto:
            print(f"Editando o produto: {produto[1]}")
            novo_nome = input("Novo nome (deixe em branco para manter): ") or produto[1]
            novo_preco_atacadao = input(
                f"Novo preço Atacadão (atual: R${produto[2]:.2f}): "
            ) or produto[2]
            novo_preco_acai = input(
                f"Novo preço Açaí (atual: R${produto[3]:.2f}): "
            ) or produto[3]
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

def remover_produto(conn):
    listar_produtos(conn)
    cursor = conn.cursor()
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

def adicionar_ao_carrinho(conn, carrinho, produto_id, quantidade):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
    produto = cursor.fetchone()

    if produto:
        nome, preco_atacadao, preco_acai = produto[1], produto[2], produto[3]

        if preco_atacadao == 0 or preco_acai == 0:
            print(f"O produto '{nome}' não está disponível em um dos supermercados.")
            escolha = input("Deseja substituir por outro que tenha preço em ambos? (s/n): ").strip().lower()
            
            if escolha == 's':
                cursor.execute("SELECT * FROM produtos WHERE preco_atacadao > 0 AND preco_acai > 0")
                produtos_disponiveis = cursor.fetchall()
                
                if not produtos_disponiveis:
                    print("Não há produtos disponíveis em ambos os supermercados.")
                    return
                
                print("\nProdutos disponíveis:")
                for p in produtos_disponiveis:
                    print(f"{p[0]} - {p[1]} (Atacadão: R${p[2]}, Açaí: R${p[3]})")

                novo_id = input("Digite o ID do novo produto: ")
                cursor.execute("SELECT * FROM produtos WHERE id = ?", (novo_id,))
                novo_produto = cursor.fetchone()

                if novo_produto:
                    carrinho.append({"produto": novo_produto, "quantidade": quantidade})
                    print(f"Substituído por: {novo_produto[1]} (x{quantidade})")
                else:
                    print("ID inválido. Nenhuma alteração feita.")
            return
        
        carrinho.append({"produto": produto, "quantidade": quantidade})
        print(f"Adicionado: {nome} (x{quantidade})")
    else:
        print("Produto não encontrado.")



def calcular_total(carrinho):
    total_atacadao = sum(item["produto"][2] * item["quantidade"] for item in carrinho)
    total_acai = sum(item["produto"][3] * item["quantidade"] for item in carrinho)
    return total_atacadao, total_acai
