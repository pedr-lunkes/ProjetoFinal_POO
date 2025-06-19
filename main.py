from unidade import Unidade
from menu import Menu
from jupiterweb import JupiterWeb

# Menu
from tqdm import tqdm
import sys


def main():
    num_unidades = 0
    if len(sys.argv) not in [1, 2]:
        print("Modo de uso: python3 main.py (numero de unidades tratadas)")
        return

    print("Inicializando Menu...")
    menu = Menu()
    menu.limpar_console()
    menu.imprimirBarras("Extraindo informações do JupiterWeb, aguarde.")
    jupiterweb = JupiterWeb()

    unidades = jupiterweb.listar_unidades()
    if len(sys.argv) == 1:
        num_unidades = len(unidades)
    else:
        num_unidades = int(sys.argv[1])

    for unidade in tqdm(unidades[:num_unidades], desc="Unidades", leave=False):
        u = Unidade(unidade)  
        cursos = jupiterweb.lista_cursos(unidade)
        
        for curso in tqdm(cursos, desc=f"Cursos ({unidade[:15]}...)", leave=False):
            if jupiterweb.selecionarCurso(curso):
                c = jupiterweb.pegarInformacoesCurso(curso, unidade)
                u.add_curso(c)

            jupiterweb.add_unidade(u)

    jupiterweb.close()

    menu.limpar_console()
    menu.imprimirBarras("Informações extraídas com sucesso.")
    menu.principal(jupiterweb)


if __name__ == "__main__":
    main()
