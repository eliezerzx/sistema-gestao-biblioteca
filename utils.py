import os

VERMELHO = "\033[1;31m"
VERDE = "\033[1;32m"
RESET = "\033[0m"

def mostrar_abertura():
    banner_vermelho = """\033[91m 
        ____________________________________________________
        |                                                    |
        |    [!] SISTEMA DE GERENCIAMENTO DE LIVROS [!]      |
        |____________________________________________________|
        |                                                    |
        |        _______                                     |
        |       /      //                                    |
        |      /      //       LISTAGEM E CADASTRO           |
        |     /______//           DE EXEMPLARES              |
        |    (______)                                        |
        |____________________________________________________|
        \033[0m"""
    print(banner_vermelho)

def exibir_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    menu_ascii = f"""{VERMELHO}
    ==================================================
    ||                                              ||
    ||   S I S T E M A   D E   C A D A S T R O      ||
    ||                D E   L I V R O S             ||
    ||                                              ||
    ==================================================
    ||                                              ||
    ||  [1] Adicionar novos livros                  ||
    ||  [2] Listar todos os livros                  ||
    ||  [3] Buscar livros                           ||
    ||  [4] Exportar dados para CSV                 ||
    ||  [5] Remover livro do sistema                ||
    ||  [6] Editar informações de livro             ||
    ||  [7] Emprestimo de livro                     ||
    ||  [8] Devolução de livro                      ||
    ||  [9] Estatísticas da biblioteca              ||           
    ||  [10] Sair do programa                       ||
    ||                                              ||
    ==================================================
    {RESET}"""
    
    print(menu_ascii)

    

