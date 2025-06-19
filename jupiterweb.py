from curso import Curso
from disciplina import Disciplina
from unidade import Unidade

# WebScraping
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from typing import List


class JupiterWeb():
    def __init__(self):
        self.disciplinas: List[Disciplina] = []
        self.cursos: List[Curso] = []
        self.unidades: List[Unidade] = []

        self.link = "https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275"
        
        chrome_options = Options()
        chrome_options.page_load_strategy = 'eager'
        chrome_options.add_argument("--headless") # Comentar abrir o chrome
        chrome_options.add_argument("--enable-automation")
        chrome_options.add_argument("--disable-client-side-phishing-detection")
        chrome_options.add_argument("--disable-component-extensions-with-background-pages")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-features=InterestFeedContentSuggestions")
        chrome_options.add_argument("--disable-features=Translate")
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--disable-search-engine-choice-screen")
        chrome_options.add_argument("--disable-images")
        
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
        
        WebDriverWait(self.driver, 5).until(
            lambda driver: len(Select(driver.find_element(By.ID, "comboUnidade")).options) > 1
        )

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

        try:
            # Checa se há mais uma opção na barra de curso
            WebDriverWait(self.driver, 5).until(
                lambda d: len(Select(d.find_element(By.ID, "comboCurso")).options) > 1
            )

            # Entrai todos os cursos e insere no objeto Unidade
            curso_select_element = self.driver.find_element(By.ID, "comboCurso")
            self.curso_select = Select(curso_select_element)

            cursos = [x.text for x in self.curso_select.options][1::]

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
            WebDriverWait(self.driver, 3).until(
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
                WebDriverWait(self.driver, 3).until(
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
    def pegarInformacoesCurso(self, nome, unidade):
        botaoGrade = self.driver.find_element(By.ID, "step4-tab")
        botaoGrade.click()
        
        try:
            WebDriverWait(self.driver, 5).until(
                lambda driver: driver.find_element(By.ID, "step4-tab").is_displayed()
            )
        except Exception as e:
            print("Erro ao buscar o elemento 'step4-tab':", e)
        
        html_step4 = self.driver.find_element(By.ID, "step4").get_attribute("innerHTML")
        soup = BeautifulSoup(html_step4, "html.parser")

        duracao_ideal = soup.find("span", {"class": "duridlhab"}).get_text()
        duracao_min = soup.find("span", {"class": "durminhab"}).get_text()
        duracao_max = soup.find("span", {"class": "durmaxhab"}).get_text()

        curso = Curso(nome, unidade, duracao_ideal, duracao_min, duracao_max)
        self._formataInfo(curso)


        botaoBuscar = self.driver.find_element(By.ID, "step1-tab")
        botaoBuscar.click()
        
        try:
            WebDriverWait(self.driver, 5).until(
                lambda driver: driver.find_element(By.ID, "step1-tab").is_displayed()
            )
        except Exception as e:
            print("Erro ao buscar o elemento 'step1-tab':", e)

        self.cursos.append(curso)
        return curso

    def _formataInfo(self, curso : Curso):  
        """
        Função que cadastra as disciplinas, que estão em formato de tabela no site    
        """
        # Espera para poder interagir com o site novamente
        try:
            WebDriverWait(self.driver, 10).until_not(
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
    
    def add_unidade(self, unidade:Unidade):
        self.unidades.append(unidade)

    def imprimir_unidades(self):
        for u in self.unidades:
            print(u.nome)
    
    def imprimir_cursos(self):
        for u in self.unidades:
            print(u)
    