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
