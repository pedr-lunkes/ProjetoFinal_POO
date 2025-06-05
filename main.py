from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


class JupiterWeb():
    def __init__(self):
        self.link = "https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275"
        
        chrome_options = Options()
        chrome_options.add_argument("--headless") 
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275")

        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.find_element(By.ID, "comboUnidade").is_displayed()
            )
        except Exception:
            print("Site não carregou")
            self.driver.quit()

    def listar_unidades(self):
        unidade_select_element = self.driver.find_element(By.ID, "comboUnidade")
        unidade_select = Select(unidade_select_element)

        unidades = [x.text for x in unidade_select.options][1::]

        return unidades

    def lista_cursos(self, unidade):
        unidade_select_element = self.driver.find_element(By.ID, "comboUnidade")
        unidade_select = Select(unidade_select_element)
        unidade_select.select_by_visible_text(unidade)

        try:
            WebDriverWait(self.driver, 5).until(
                lambda driver: len(Select(driver.find_element(By.ID, "comboCurso")).options) > 1
            )

            curso_select_element = self.driver.find_element(By.ID, "comboCurso")
            self.curso_select = Select(curso_select_element)

            cursos = [x.text for x in self.curso_select.options][1::]

            return cursos
        except Exception:
            print("Curso não carregado para a unidade:", unidade)

            return
        
    def selecionarCurso(self, curso):
        self.curso_select.select_by_visible_text(curso)
        self.buscar()
        
    def buscar(self):
        botaoBuscar = self.driver.find_element(By.ID, "enviar")
        botaoBuscar.click()

        try:
            WebDriverWait(self.driver, 5).until(
                lambda driver: driver.find_element(By.ID, "step4-tab").is_displayed()
            )
        except Exception as e:
            print("Erro ao buscar o elemento 'step4-tab':", e)

        return

    def retornarInformacoes(self):
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
        self._formataInfo(soup)

        botaoBuscar.click()
        
        try:
            WebDriverWait(self.driver, 5).until(
                lambda driver: driver.find_element(By.ID, "step1-tab").is_displayed()
            )
        except Exception as e:
            print("Erro ao buscar o elemento 'step1-tab':", e)

        return

    def _formataInfo(self, soup):
        duracao_ideal = soup.find("span", {"class": "duridlhab"}).get_text()
        duracao_min = soup.find("span", {"class": "durminhab"}).get_text()
        duracao_max = soup.find("span", {"class": "durmaxhab"}).get_text()

        # To search for multiple divs with BeautifulSoup, use find_all:
        div = soup.find("div", {"id": "gradeCurricular"})
        print(div)

        tabelas = div.find_all("table")

        print(tabelas)

        # for div in divs:
        #     print(div)
        #     tabelas = div.find_all("table")
        #     for tabela in tabelas:
        #         print(tabela.prettify())

        # for t in tabelas:
        #     trs = t.tbody.find_all("tr")

        #     nomeTab = trs[0].find("td").get_text()

            # print(nomeTab)    

        print(duracao_ideal, duracao_min, duracao_max)

    def close(self):
        self.driver.quit()


def main():
    jupiterweb = JupiterWeb()

    # unidades = jupiterweb.listar_unidades()

    # for unidade in unidades:
    #     print(f"Unidade {unidade}:")
        
    #     cursos = jupiterweb.lista_cursos(unidade)
        
    #     for curso in cursos:
    #         jupiterweb.selecionarCurso(curso)
    #         jupiterweb.retornarInformacoes()


    # ------------ TESTE DE UM CURSO SÓ ----------------
    unidades = jupiterweb.listar_unidades()

    while(len(unidades) == 0):
        unidades = jupiterweb.listar_unidades()

    cursos = jupiterweb.lista_cursos(unidades[0])
    jupiterweb.selecionarCurso(cursos[0])
    jupiterweb.retornarInformacoes()

    jupiterweb.close()
    

if __name__ == "__main__":
    main()
