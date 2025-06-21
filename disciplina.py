# Grupo composto por:
# Pedro Henrique de Sousa Prestes	15507819
# Pedro Henrique Perez Dias		15484075
# Pedro Lunkes Villela			15484287

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

    def cursos_da_disciplina(self):
        cursos_str = '\n---------------------\n'.join(str(curso) for curso in self.cursos)
        return cursos_str

    def __str__(self):
        valor = f"""Código: {self.cod} \nNome: {self.nome} 
Créditos-Aula: {self.cred_aula} \nCréditos-Trabalho: {self.cred_aula} 
Carga Horária: {self.carga_horaria} \nCarga Estágio: {self.carga_estagio} 
Carga Práticas: {self.carga_praticas} \nAtividades: {self.atividades} \n"""
        return valor