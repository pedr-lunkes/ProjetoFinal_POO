# Grupo composto por:
# Pedro Henrique de Sousa Prestes	15507819
# Pedro Henrique Perez Dias		15484075
# Pedro Lunkes Villela			15484287

class Unidade():
    def __init__(self, nome):
        self.nome = nome
        self.cursos = []

    def add_curso(self, curso):
        self.cursos.append(curso)

    def __str__(self):
        nomeUnidade = f"{self.nome}\n"
        cursos_str = '\n---------------------\n'.join(str(curso) for curso in self.cursos)
        return nomeUnidade + cursos_str