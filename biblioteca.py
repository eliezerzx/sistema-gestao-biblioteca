import csv
import json
import os
from utils import VERMELHO, VERDE, RESET
from tabulate import tabulate
from tqdm import tqdm 
import time

livros = []


def inicializar_sistema():
    # Cria as pastas necessárias caso não existam
    pastas = ["dados", "exports"]
    for pasta in pastas:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"{VERDE}[✓] Pasta '{pasta}' criada com sucesso [✓]{RESET}")

inicializar_sistema()

def salvar_dados():
    with open("dados/livros.json", "w", encoding="utf-8") as arquivo:
        json.dump(livros, arquivo, ensure_ascii=False, indent=4)

def carregar_dados():
    global livros
    try:
        with open("dados/livros.json", "r", encoding="utf-8") as arquivo:
            livros = json.load(arquivo)

            for livro in livros:
                livro["id"] = int(livro["id"])

    except FileNotFoundError:
        livros = []
# 
def gerar_id():
    if not livros:
        return 1 # Retorna 1 se ainda não há livros
    return max(livro["id"] for livro in livros) + 1 # Pega o maior ID existente e soma +1 se já houver livros

def adicionar_livro(nome, autor, paginas):
    livro = {
        "id": gerar_id(),
        "nome": nome,
        "autor": autor,
        "paginas": paginas,
        "status": "disponível", 
        "cliente": None
    }
    livros.append(livro)
    salvar_dados()
    print("=============== LIVRO CADASTRADO! ===============")
    print(f"=============== ID: {livro['id']} ===============")

def remover_livro(id_livro):
    for livro in livros:
        if int(livro.get("id", 0)) == int(id_livro):
            livros.remove(livro)
            salvar_dados()
            print("\n=============== Livro removido com sucesso! ===============")
            return
    print("==========================================")
    print("Livro não encontrado.")

def buscar_livro(id_livro):
    for livro in livros:
        if int(livro.get("id", 0)) == int(id_livro):
            # Garante que o status e cliente existam antes de retornar
            if "status" not in livro:
                livro["status"] = "disponível"
            if "cliente" not in livro:
                livro["cliente"] = None
            return livro
    return None

def buscar_por_nome(nome):
    resultados = [l for l in livros if nome.lower() in l["nome"].lower()]
    return resultados

def editar_livro(id_livro):
    livro = buscar_livro(id_livro)

    if livro:
        novo_nome = input("Nome: ")
        novo_autor = input("Autor: ")
        novas_paginas = int(input("Paginas: "))

        livro["nome"] = novo_nome
        livro["autor"] = novo_autor
        livro["paginas"] = novas_paginas
        salvar_dados()

        print("=============== LIVRO ATUALIZADO! ===============")
    else:
        print("==========================================")
        print("Livro não encontrado.")

def listar_livros():
    if not livros:
        print(f"\n{VERMELHO}=========================================={RESET}")
        print("Nenhum livro cadastrado.")
    else:
        # Preparamos os dados para a tabela
        tabela = []
        for livro in livros:
            status = livro.get("status", "disponível")
            cliente = livro.get("cliente", "---")
            
            # Aplicamos cores direto nos dados da tabela
            status_cor = f"{VERDE}Disponível{RESET}" if status == "disponível" else f"{VERMELHO}Emprestado ({cliente}){RESET}"
            
            tabela.append([
                livro['id'], 
                livro['nome'], 
                livro['autor'], 
                livro['paginas'], 
                status_cor
            ])
        
        # Exibimos a tabela formatada
        cabecalhos = ["ID", "Título", "Autor", "Páginas", "Status"]
        print("\n" + tabulate(tabela, headers=cabecalhos, tablefmt="grid"))
            

def mostrar_estatisticas():
    if not livros:
        print("\n==========================================")
        print("===== Nenhum livro cadastrado para analisar. =====")
        return
    
    total_livros = len(livros)
    # Conta quantos livros tem o status 'emprestado'
    livros_emprestados = len([l for l in livros if l.get("status") == "emprestado"])
    livros_disponiveis = total_livros - livros_emprestados

    total_paginas = sum(livro["paginas"] for livro in livros)
    media_paginas = total_paginas / total_livros

    maior_livro = max(livros, key=lambda livro: livro["paginas"])
    menor_livro = min(livros, key=lambda livro: livro["paginas"])

    print("\n========== ESTATÍSTICAS DA BIBLIOTECA ==========")
    print(f"Total de exemplares: {total_livros}")
    # Adicionamos as novas métricas com cores para destaque
    print(f"Livros Disponíveis: {VERDE}{livros_disponiveis}{RESET}")
    print(f"Livros Emprestados: {VERMELHO}{livros_emprestados}{RESET}")
    print(f"Taxa de ocupação: {(livros_emprestados/total_livros)*100:.1f}%")
    print("-" * 40)
    print(f"Total de páginas no acervo: {total_paginas}")
    print(f"Média de páginas por livro: {media_paginas:.2f}")
    print(f"Maior livro: {maior_livro['nome']} ({maior_livro['paginas']} pág.)")
    print(f"Menor livro: {menor_livro['nome']} ({menor_livro['paginas']} pág.)")
    print("\n========== ESTATÍSTICAS DA BIBLIOTECA ==========")

def emprestar_livro(id_livro, nome_cliente):
    livro = buscar_livro(id_livro)
    if livro:
        if livro["status"] == "disponível":
            livro["status"] = "emprestado"
            livro["cliente"] = nome_cliente
            salvar_dados()
            print(f"\n[OK] Livro {livro['nome']}' emprestado para {nome_cliente}")
        else:
            print(f"\n[!] Este livro já está emprestado para {livro['cliente']} [!]")
            print("=============================================================")
            print("\n========== Para consultar o stutus: ==========")
            print("     >>>>> [2] Listar todos os livros <<<<<")
            print("     ========== Ou procure em: ==========")
            print("         >>>>> [3] Buscar livros <<<<<")
            print("\n=============================================================")
    else:
            print("\n [!] Livro não encontrado [!]")

def devolver_livro(id_livro):
    livro = buscar_livro(id_livro)
    if livro:
        if livro["status"] == "emprestado":
            livro["status"] = "disponível"
            livro["cliente"] = None
            salvar_dados()
            print(f"\n[OK] Livro '{livro['nome']}' devolvido com sucesso [!] ")
        else:
            print("\n[!] Este livro já está na biblioteca [!]")
    else:
        print("\n[!] Livro não encontrado [!]")

def exportar_csv(nome_arquivo="exports/livros.csv"):
    import os
    os.makedirs("exports", exist_ok=True)

    print(f"\n{VERDE}Iniciando exportação...{RESET}")
    
    # Criamos a barra de progresso baseada na quantidade de livros
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["Id", "Livro", "Autor", "Paginas", "Status", "Cliente"])

        # O tqdm envolve o loop e mostra a barra conforme ele avança
        for livro in tqdm(livros, desc="Exportando exemplares", unit="livro"):
            time.sleep(0.1) # Simula um pequeno atraso para a barra ser visível
            status = livro.get("status", "disponível")
            cliente = livro.get("cliente", "N/A")
            
            escritor.writerow([
                livro["id"], livro["nome"], livro["autor"], 
                livro["paginas"], status, cliente
            ])
            
    print(f"\n{VERDE}✓ Dados exportados com sucesso para: {nome_arquivo}{RESET}")