import os
from rapidfuzz import process
import spacy
import shutil

class Menu():
    def __init__(self):
        self.nlp = spacy.load("pt_core_news_sm")

    @staticmethod
    def limpar_console() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def imprimirBarras(string) -> None:
        barra = shutil.get_terminal_size()[0] * '=' # Adequa o tamanho da linha ao tamanho do terminal
        espacos = ((len(barra) - len(string))//2) * ' '
        print('\n' + barra)
        print(espacos + string + espacos)
        print(barra)

    def normalizar_termo(self, termo) -> str:
        # termo = termo.lower() - Normalização para minúscula, não dá certo
        doc = self.nlp(termo)
        lema = " ".join([token.lemma_ for token in doc])
        return lema
    
    def busca_campo(self, local_busca):
        termo_busca = self.normalizar_termo(input())
        nomes = [campo.nome for campo in local_busca]

        # Obter TODOS os matches com score > 60
        matches = process.extract(
            termo_busca, 
            nomes, 
            score_cutoff=60
        )

        # Se alguma unidade tiver semelhança de pelo menos 60%, retorna aquela unidade
        return matches
    
    # MENU PRINCIPAL
    def principal(self, jupiterweb) -> None:
        while (True):
            self.imprimirBarras("Escolha uma operação:")

            # Funcionalidades
            print("1. Listar Unidades")
            print("2. Listar todos os Cursos")
            print("3. Listar Cursos dado uma Unidade")
            print("4. Listar Dados de um Curso")
            print("5. Dados de uma disciplina")
            print("6. Disciplinas que são usadas em mais de um curso")
            print("7. Sair")

            comando = input('-> ')
            self.limpar_console()

        # Coisas para fazer aqui Perez
        # Listar Unidades
            if comando == '1':
                self.imprimirBarras("Unidades")

                # Melhora a função de imprimir unidades pra imprimir elas bonitinho

                jupiterweb.imprimir_unidades()

            # Listar todos os Cursos
            elif comando == '2':
                self.imprimirBarras("Cursos")

                # Mesma coisa da de cima, só que pra cursos

                jupiterweb.imprimir_cursos()

        # Listar Cursos dado uma Unidade
            elif comando == '3':
                self.imprimirBarras("Escreva o nome da Unidade que você deseja consultar:")
            
                termo_busca = self.normalizar_termo(input('-> '))
                dic_unidades = {unidade.nome: unidade for unidade in jupiterweb.unidades}

                # Obter TODOS os matches com score > 60
                matches = process.extract(
                    termo_busca, 
                    list(dic_unidades.keys()),
                    score_cutoff=60
                )

                if matches:
                    if len(matches) != 1:
                        self.imprimirBarras("Insira o número correspondente na lista abaixo")
                        for i, match in enumerate(matches):
                            print(f'{i+1}.{match[0]}')
                        try:
                            indice = int(input('\n-> '))
                            unidade = dic_unidades[matches[indice - 1][0]].nome
                            print(unidade) # debug
                        except:
                            self.imprimirBarras("Erro: índice inválido")

                    else:
                        unidade = dic_unidades[matches[0][0]].nome
                        print(unidade) # debug
                else:
                    self.imprimirBarras("Nenhuma unidade correspondente encontrada.")

                # TEM QUE PRINTAR OS CURSOS DA UNIDADE PEDRO PEREZ

        # Listar dados de um curso:
            elif comando == '4':
                self.imprimirBarras("Escreva o nome do Curso que você deseja consultar:")
            
                termo_busca = self.normalizar_termo(input('-> '))
                dic_cursos = {}
                for unidade in jupiterweb.unidades:
                    for curso in unidade.cursos:
                        dic_cursos[curso.nome + '-' + unidade.nome] = curso

                # Obter TODOS os matches com score > 60
                matches = process.extract(
                    termo_busca, 
                    list(dic_cursos.key()),
                    score_cutoff=60
                )

                if matches:
                    if len(matches) != 1:
                        self.imprimirBarras("Insira o número correspondente na lista abaixo")
                        for i, match in enumerate(matches):
                            print(f'{i+1}.{match[0]}')
                        try:
                            indice = int(input('\n-> '))
                            curso = dic_unidades[matches[indice - 1][0]].nome
                            print(curso) # debug
                        except:
                            self.imprimirBarras("Erro: índice inválido")

                    else:
                        curso = dic_unidades[matches[0][0]].nome
                        print(curso)

                    # TEM QUE PRINTAR OS DETALHES DO CURSO PEDRO PEREZ
                else:
                    self.imprimirBarras("Nenhum curso correspondente encontrado.")
                
        # Listar dados de uma disciplina
            elif comando == '5':
                print("Se quiser eu faço pedro perez")

        # Disciplinas que são usadas em mais de um curso (que negócio específico)
            elif comando == '6':
                print("Faça Pedro Perez")
            
        # Sair do programa
            elif comando == '7':
                self.imprimirBarras("Encerrando...")
                return
        
        # Comando inválido
            else:
                continue

            self.imprimirBarras("Pressione ENTER para voltar ao menu")
            input()
            self.limpar_console()