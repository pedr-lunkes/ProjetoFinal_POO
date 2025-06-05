class Disciplina():
    def __init__(self, cod, nome, cred_aula, cred_trab, carga_horaria, carga_estagio, carga_praticas, atividades, curso):
        self.cod = cod
        self.nome = nome
        self.cred_aula = cred_aula
        self.cred_trab = cred_trab
        self.carga_horaria = carga_horaria
        self.carga_estagio = carga_estagio
        self.carga_praticas = carga_praticas
        self.atividades = atividades
        
        self.cursos = []
        self.cursos.append(curso)

    def add_curso(self, curso):
        self.cursos.append(curso)