class Curso():
    def __init__(self, nome, unidade, duracao_ideal, duracao_min, duracao_max):
        self.nome = nome
        self.unidade = unidade
        self.duracao_ideal = duracao_ideal
        self.duracao_min = duracao_min
        self.duracao_max = duracao_max
        self.disc_obrigatorias = []
        self.disc_op_livres = []
        self.disc_op_eletivas = []

    def add_obrigatoria(self, obrigatoria):
        self.disc_obrigatorias.append(obrigatoria)

    def add_livre(self, livre):
        self.disc_op_livres.append(livre)

    def add_eletivas(self, eletiva):
        self.disc_op_eletivas.append(eletiva)

    def str_disciplinas(self, disciplinas):
        val = "["
        cursos_str = ', '.join(str(d.nome) for d in disciplinas)
        val += cursos_str + "]"
        return val

    def __str__(self):
        valor = f"""Curso: {self.nome} \nUnidade: {self.unidade}
Duração Ideal: {self.duracao_ideal} \nDuração Minima: {self.duracao_min} 
Duração Maxima: {self.duracao_max} \nDisciplinas Obrigatorias: {self.str_disciplinas(self.disc_obrigatorias)} 
Disciplinas Eletivas: {self.str_disciplinas(self.disc_op_eletivas)} 
Disciplinas Optativas Livres: {self.str_disciplinas(self.disc_op_livres)}"""
        return valor