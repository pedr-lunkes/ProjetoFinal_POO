class Unidade():
    def __init__(self, nome):
        self.nome = nome
        self.cursos = []

    def add_curso(self, curso):
        self.cursos.append(curso)
