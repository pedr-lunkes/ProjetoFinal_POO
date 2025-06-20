# Grupo composto por:
# Pedro Henrique de Sousa Prestes	15507819
# Pedro Henrique Perez Dias		15484075
# Pedro Lunkes Villela			15484287

import os
from rapidfuzz import process
import spacy
import shutil
from collections import defaultdict
from grafo import Grafo

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
        doc = self.nlp(termo)
        lema = " ".join([token.lemma_ for token in doc])
        return lema
    
    # MENU PRINCIPAL
    def principal(self, jupiterweb) -> None:
        while (True):
            self.imprimirBarras("Escolha uma operação:")

            # Funcionalidades
            print("1. Listar Unidades")
            print("2. Listar todos os Cursos")
            print("3. Listar Cursos dado uma Unidade")
            print("4. Listar dados de um Curso")
            print("5. Listar dados de uma Disciplina")
            print("6. Listar Disciplinas que são usadas em mais de um Curso")
            print("7. Criar um Grafo dos Cursos baseado nas Disciplinas em comum")
            print("8. Sair")

            comando = input('-> ')
            self.limpar_console()

        # Listar Unidades
            if comando == '1':
                self.imprimirBarras("Unidades")

                jupiterweb.imprimir_unidades()

        # Listar todos os Cursos
            elif comando == '2':
                self.imprimirBarras("Cursos")

                jupiterweb.imprimir_cursos()

        # Listar Cursos dado uma Unidade
            elif comando == '3':
                self.imprimirBarras("Escreva o nome da Unidade que você deseja consultar:")
            
                termo_busca = self.normalizar_termo(input('-> '))
                dic_unidades = {unidade.nome: unidade for unidade in jupiterweb.unidades}

                matches = process.extract(
                    termo_busca, 
                    list(dic_unidades.keys()),
                    score_cutoff=60,
                    limit=None
                )

                if matches:
                    if len(matches) != 1:
                        self.imprimirBarras("Insira o número correspondente na lista abaixo")
                        for i, match in enumerate(matches):
                            print(f'{i+1}.{match[0]}')
                        try:
                            indice = int(input('\n-> '))
                            unidade = dic_unidades[matches[indice - 1][0]]
                            print(unidade)
                        except:
                            self.imprimirBarras("Erro: índice inválido")

                    else:
                        unidade = dic_unidades[matches[0][0]]
                        print(unidade)
                else:
                    self.imprimirBarras("Nenhuma unidade correspondente encontrada.")

        # Listar dados de um Curso:
            elif comando == '4':
                self.imprimirBarras("Escreva o nome do Curso que você deseja consultar:")
            
                termo_busca = self.normalizar_termo(input('-> '))
                dic_cursos = {}
                for curso in jupiterweb.cursos:
                    dic_cursos[f'{curso.nome} da {curso.unidade}'] = curso

                matches = process.extract(
                    termo_busca, 
                    list(dic_cursos.keys()),
                    score_cutoff=60,
                    limit=None
                )

                if matches:
                    if len(matches) != 1:
                        self.imprimirBarras("Insira o número correspondente na lista abaixo")
                        for i, match in enumerate(matches):
                            print(f'{i+1}.{match[0]}')
                        try:
                            indice = int(input('\n-> '))
                            curso = dic_cursos[matches[indice - 1][0]]
                            print(curso)
                        except:
                            self.imprimirBarras("Erro: índice inválido")

                    else:
                        curso = dic_cursos[matches[0][0]]
                        print(curso)

                else:
                    self.imprimirBarras("Nenhum curso correspondente encontrado.")
                
        # Listar dados de uma Disciplina
            elif comando == '5':
                self.imprimirBarras("Escreva o nome da Disciplina que você deseja consultar:")

                termo_busca = self.normalizar_termo(input('-> '))
                dic_disciplinas = {f'{disciplina.cod} - {disciplina.nome}': disciplina for disciplina in jupiterweb.disciplinas}

                matches = process.extract(
                    termo_busca, 
                    list(dic_disciplinas.keys()),
                    score_cutoff=80,
                    limit=None
                )

                if matches:
                    if len(matches) != 1:
                        self.imprimirBarras("Insira o número correspondente na lista abaixo")
                        for i, match in enumerate(matches):
                            print(f'{i+1}.{match[0]}')
                        try:
                            indice = int(input('\n-> '))
                            disciplina = dic_disciplinas[matches[indice - 1][0]]
                            print(disciplina)
                        except:
                            self.imprimirBarras("Erro: índice inválido")

                    else:
                        disciplina = dic_disciplinas[matches[0][0]]
                        print(disciplina)

        # Disciplinas que são usadas em mais de um curso
            elif comando == '6':
                aparicoesCurso = defaultdict(int)
                for disciplina in jupiterweb.disciplinas:
                    for curso in disciplina.cursos:
                        aparicoesCurso[curso.nome] += 1
                        if aparicoesCurso[curso.nome] == 2:
                            print(f"{curso.unidade}: {disciplina.nome}")

        # Grafo
            elif comando == '7':
                self.imprimirBarras("Gerando Grafo. Isso pode demorar um pouco...")
                grafo_cursos = Grafo(jupiterweb.cursos)
                grafo_cursos.plotar_grafo()
                
        # Sair do programa
            elif comando == '8':
                self.imprimirBarras("Encerrando...")
                return
        
        # Comando inválido
            else:
                continue

            self.imprimirBarras("Pressione ENTER para voltar ao menu")
            input()
            self.limpar_console()