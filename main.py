from utils import mostrar_abertura, exibir_menu, VERMELHO, VERDE, RESET
from biblioteca import (
    adicionar_livro,
    adicionar_livro,
    remover_livro,
    buscar_livro,
    buscar_por_nome,
    editar_livro,
    listar_livros,
    exportar_csv,
    carregar_dados,
    mostrar_estatisticas,
    emprestar_livro,
    devolver_livro
)

mostrar_abertura()
carregar_dados()
input("Pressione Enter para continuar...")

while True:
    exibir_menu()

    opcao = input(f"{VERMELHO}Escolha uma opção: {RESET}")

    if opcao == "1":
        nome = input("Livro: ").strip()

        if not nome.strip():
            print("!!! Nome do livro não pode estar vazio !!!")
            input("\nPressione Enter para voltar ao menu...")
            continue

        autor = input("Autor: ").strip()

        if not autor:
            print("!!! Nome do autor não pode estar vazio !!!")
            input("\nPressione Enter para voltar ao menu...")
            continue

        try:
            paginas = int(input("Paginas: "))
            if paginas <= 0:
                print("========== Digite um numero maior que zero! ==========")
                input("\nPressione Enter para voltar ao menu...")
                continue

            adicionar_livro(nome, autor, paginas)

        except ValueError:
            print("========== !! Numero invalido !! ==========")
            input("\nPressione Enter para voltar ao menu...")
            continue

        input("\nPressione Enter para voltar ao menu...")

    elif opcao == "2":
        listar_livros()
        input("\nPressione Enter para voltar ao menu...")

    elif opcao == "3":
        entrada = input("Digite o ID ou o Nome do livro para buscar: ").strip()
        
        # Identifica se a busca é por ID (se forem apenas números) ou por Nome
        if entrada.isdigit():
            resultado_id = buscar_livro(int(entrada))
            # Transformamos em lista para que o loop de exibição abaixo funcione igual para ambos
            resultados = [resultado_id] if resultado_id else []
        else:
            resultados = buscar_por_nome(entrada)

        # Exibição dos resultados encontrados
        if resultados:
            print(f"\n{VERDE}========== {len(resultados)} LIVRO(S) ENCONTRADO(S) =========={RESET}")
            for livro in resultados:
                status = livro.get("status", "disponível")
                cliente = livro.get("cliente")
                
                if status == "disponível":
                    status_exibir = f"{VERDE}[ DISPONÍVEL ]{RESET}"
                else:
                    status_exibir = f"{VERMELHO}[ EMPRESTADO para: {cliente} ]{RESET}"

                print(f"Status: {status_exibir}")
                print(f"ID: {livro['id']} | Nome: {livro['nome']}")
                print(f"Autor: {livro['autor']} | Páginas: {livro['paginas']}")
                print("-" * 45)
        else:
            print(f"\n{VERMELHO}[!] Nenhum livro encontrado para: '{entrada}'{RESET}")

        input("\nPressione Enter para voltar ao menu...")

    elif opcao == "4":
        exportar_csv()
        input("\nPressione Enter para voltar ao menu...")

    elif opcao == "5":
        print("==========================================")
        id_livro = int(input("\nDigite o ID do livro para remover: "))
        remover_livro(id_livro)
        input("\nPressione Enter para voltar ao menu...")

    elif opcao == "6":
        print("==========================================")
        id_entrada = input("Digite o ID para editar: ")
        try:
            # Tenta converter para inteiro
            id_livro = int(id_entrada)
            # Se a conversao der certo, ele executa a função
            editar_livro(id_livro)
        except ValueError:
            print("\n===== !!! Erro: ID inválido. Por favor, digite apenas números !!! =====")
            print("\n Para consultar o ID do livro basta ir para: \n   >>>>> [2] Listar todos os livros <<<<<")

        input("\nPressione Enter para voltar ao menu...")

    elif opcao == "7":
        try:
            id_livro = int(input("ID do livro para emprestimo: "))
            nome_cliente = input("Nome do cliente: ").strip()
            if nome_cliente:
                emprestar_livro(id_livro, nome_cliente)
            else:
                print("[!] Nome do cliente é obrigatório [!]")
        except ValueError:
            print("===== !!! ID inválido !!! =====")
        input("\nPressione Enter para voltar ao menu...")
    
    elif opcao == "8":
        try:
            id_livro = int(input("Id do livro para devolução: "))
            devolver_livro(id_livro)
        except ValueError:
            print("===== !!! ID inválido !!! =====")
        input("\nPressione Enter para voltar ao menu...")

    elif opcao == "9":
        mostrar_estatisticas()
        input("\nPressione Enter para voltar ao menu...")

    elif opcao == "10":
        print("=================== Saindo do sistema... ===================")
        break

    else:
        print("\n=================== !! Opção inválida !! ===================")
        input("\nPressione Enter para voltar ao menu...")