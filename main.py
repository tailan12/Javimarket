from util import conectar_banco, criar_tabelas
from produto import adicionar_novo_produto, editar_produto, remover_produto
from cliente import cadastrar_usuario, login_usuario

def menu_administrador(cursor, conn):
    while True:
        print("\nMenu do Administrador:")
        print("1. Adicionar produtos")
        print("2. Editar produtos")
        print("3. Remover produtos")
        print("4. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_novo_produto(cursor, conn)
        elif opcao == "2":
            editar_produto(cursor, conn)
        elif opcao == "3":
            remover_produto(cursor, conn)
        elif opcao == "4":
            break
        else:
            print("Opção inválida. Tente novamente.")

def main():
    conn, cursor = conectar_banco()
    criar_tabelas(cursor, conn)
    while True:
        print("\nEscolha seu perfil:")
        print("1. Administrador")
        print("2. Cadastrar usuário")
        print("3. Login")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_administrador(cursor, conn)
        elif opcao == "2":
            cadastrar_usuario(cursor, conn)
        elif opcao == "3":
            login_usuario(cursor)
        elif opcao == "4":
            print("Encerrando...")
            break
        else:
            print("Opção inválida!")
    conn.close()

if __name__ == "__main__":
    main()
