from curso import Curso
from disciplina import Disciplina
from unidade import Unidade
from menu import Menu

import sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
from tqdm import tqdm
from typing import List

class JupiterWeb():
    def __init__(self):
        self.disciplinas: List[Disciplina] = []
        self.cursos: List[Curso] = []
        self.unidades: List[Unidade] = []

        self.link = "https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275"
        
        chrome_options = Options()
        chrome_options.add_argument("--headless") # Comentar para visualização no navegador
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.link)

        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.find_element(By.ID, "comboUnidade").is_displayed()
            ) # Tenta encontrar a barra de seleção de unidades e checar se ela aparece
        except Exception:
            print("Site não carregou ou div não foi carregada")
            self.driver.quit()
            return
        
        sleep(1) # Para dar tempo de carregar as unidades dentro do comboUnidade

        # soup = BeautifulSoup(self.driver.page_source, "html.parser")
        # with open("soup_contents.txt", "w", encoding="utf-8") as f:
        #     f.write(soup.prettify())


    # -------------------------------------------------------------------------------- #
    def listar_unidades(self):
        """
        Função que retorna uma lista com as unidades cadastradas no Jupiterweb
        """
        unidade_select_element = self.driver.find_element(By.ID, "comboUnidade")
        unidade_select = Select(unidade_select_element)

        # Pega todas as unidades, pulando o "Selecione a unidade"
        unidades = [x.text for x in unidade_select.options][1::]

        return unidades

    def lista_cursos(self, unidade):
        """
        Função que retorna uma lista com dos nomes dos cursos cadastradas na unidade especificada
        """
        unidade_select_element = self.driver.find_element(By.ID, "comboUnidade")
        unidade_select = Select(unidade_select_element)
        unidade_select.select_by_visible_text(unidade)

        # u = Unidade(unidade)

        try:
            # Checa se há mais uma opção na barra de curso
            WebDriverWait(self.driver, 5).until(
                lambda driver: len(Select(driver.find_element(By.ID, "comboCurso")).options) > 1
            )

            # Entrai todos os cursos e insere no objeto Unidade
            curso_select_element = self.driver.find_element(By.ID, "comboCurso")
            self.curso_select = Select(curso_select_element)

            cursos = [x.text for x in self.curso_select.options][1::]
            
            # for c in cursos:
            #     u.add_curso(c)

            # # Adiciona a unidade na lista de unidades da classe JupiterWeb
            # self.unidades.append(u)

            return cursos
        except Exception:
            print("Curso não carregado para a unidade:", unidade)

            return
        
    def selecionarCurso(self, curso):
        self.curso_select.select_by_visible_text(curso)

        return self.buscar()
        
    def buscar(self):
        botaoBuscar = self.driver.find_element(By.ID, "enviar")
        botaoBuscar.click()

        try: # Verifica se o elemento de erro aparece
            WebDriverWait(self.driver, 1).until(
                lambda driver: driver.find_element(By.ID, "err").is_displayed()
            )
            botoes = self.driver.find_elements(By.CSS_SELECTOR, "button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")
            for botao in botoes:
                span = botao.find_element(By.TAG_NAME, "span")  # Pega o primeiro <span>
                if span.text == 'Fechar':
                    botao.click()
            return 0
        except:
            try:
                WebDriverWait(self.driver, 1).until(
                    lambda driver: driver.find_element(By.ID, "step4-tab").is_displayed()
                )
            except Exception as e:
                print("Erro ao buscar o elemento 'step4-tab':", e)
        
        return 1
    
    def close(self):
        self.driver.quit()

    # -------------------------------------------------------------------------------- #
    # Cadastro dos Cursos e Disciplinas
    # -------------------------------------------------------------------------------- #
    def retornarInformacoes(self, nome, unidade):
        botaoGrade = self.driver.find_element(By.ID, "step4-tab")
        botaoBuscar = self.driver.find_element(By.ID, "step1-tab")
        botaoGrade.click()
        
        try:
            WebDriverWait(self.driver, 5).until(
                lambda driver: driver.find_element(By.ID, "step4-tab").is_displayed()
            )
        except Exception as e:
            print("Erro ao buscar o elemento 'step4-tab':", e)
        
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        duracao_ideal = soup.find("span", {"class": "duridlhab"}).get_text()
        duracao_min = soup.find("span", {"class": "durminhab"}).get_text()
        duracao_max = soup.find("span", {"class": "durmaxhab"}).get_text()

        curso = Curso(nome, unidade, duracao_ideal, duracao_min, duracao_max)
        self._formataInfo(curso)
        botaoBuscar.click()
        
        try:
            WebDriverWait(self.driver, 5).until(
                lambda driver: driver.find_element(By.ID, "step1-tab").is_displayed()
            )
        except Exception as e:
            print("Erro ao buscar o elemento 'step1-tab':", e)

        return curso

    def _formataInfo(self, curso : Curso):  
        """
        Função que cadastra as disciplinas, que estão em formato de tabela no site    
        """
        # Espera para poder interagir com o site novamente
        try:
            WebDriverWait(self.driver, 60).until_not(
                lambda driver: driver.find_element(By.CSS_SELECTOR, ".blockUI.blockOverlay").is_displayed()
            )
        except Exception:
            print("Overlay de carregamento não sumiu a tempo.")
            return

        # Procura e abre o innerHTML da tabela de Disciplinas
        try:
            html = self.driver.find_element(By.ID, "gradeCurricular").get_attribute("innerHTML")
            soup = BeautifulSoup(html, "html.parser")
            tabelas = soup.find_all("table")

            # Divide em tabelas para cada tipo de disciplina
            for tab in tabelas:  
                trs = tab.find_all("tr")
                tipo_disc = trs[0].get_text()
                # print(f"Tipo da disciplina: {tipo_disc}")
                
                for tr in trs[2::]:  # Pula a segunda tr porque ela é um cabecalho
                    tds = tr.find_all("td")
                    # print([x.get_text() for x in tds])

                    # Pega as informações da planilha
                    cod = tds[0].get_text()
                    if len(cod) > 7: 
                        continue

                    # Generator para ver se já existe
                    existente = next((x for x in self.disciplinas if x.cod == cod), None)
                    if existente:
                        self.add_tipo_disc(tipo_disc, curso, existente)
                        continue

                    nome = tds[1].get_text()
                    cred_aula = int(tds[2].get_text()) if tds[2].get_text() != "" else 0
                    cred_trab = int(tds[3].get_text()) if tds[3].get_text() != "" else 0
                    carga_horaria = int(tds[4].get_text()) if tds[4].get_text() != "" else 0
                    carga_estagio = int(tds[5].get_text()) if tds[5].get_text() != "" else 0
                    carga_praticas = int(tds[6].get_text()) if tds[6].get_text() != "" else 0
                    atividades = int(tds[7].get_text()) if tds[7].get_text() != "" else 0

                    # Salva nova disciplina na lista de disciplinas
                    nova_disciplina = Disciplina(cod, nome, cred_aula, cred_trab, carga_horaria, carga_estagio, carga_praticas, atividades, curso)
                    self.disciplinas.append(nova_disciplina)
                    self.add_tipo_disc(tipo_disc, curso, nova_disciplina)                    

                    return
        except Exception as e:
            print("Erro ao acessar a tabela:", e)   
            return
        
    def add_tipo_disc(self, tipo_disc, curso, nova_disciplina):
        if tipo_disc == "Disciplinas Obrigatórias":
            curso.add_obrigatoria(nova_disciplina)
        elif tipo_disc == "Disciplinas Optativas Livres":
            curso.add_livre(nova_disciplina)
        elif tipo_disc == "Disciplinas Optativas Eletivas":
            curso.add_eletivas(nova_disciplina)

        return

    # -------------------------------------------------------------------------------- #
    # Imprimir coisas
    # -------------------------------------------------------------------------------- #
    def imprimir_unidades(self):
        for u in self.unidades:
            print(u.nome)
    
    def imprimir_cursos(self):
        for u in self.unidades:
            print(u)  

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
                c = jupiterweb.retornarInformacoes(curso, unidade)
                u.add_curso(c)
                jupiterweb.cursos.append(c)
        
        jupiterweb.unidades.append(u)

    jupiterweb.close()

    menu.limpar_console()
    menu.imprimirBarras("Informações extraídas com sucesso.")
    menu.principal(jupiterweb)

    # ------------ TESTE DE UM CURSO SÓ ----------------
    # unidades = jupiterweb.listar_unidades()

    # while(len(unidades) == 0):
    #     unidades = jupiterweb.listar_unidades()

    # cursos = jupiterweb.lista_cursos(unidades[0])
    # jupiterweb.selecionarCurso(cursos[0])
    # jupiterweb.retornarInformacoes(cursos[0], unidades[0])
    

if __name__ == "__main__":
    main()
