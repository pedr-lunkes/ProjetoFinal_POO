from rapidfuzz import fuzz
import networkx as nx
import spacy
import matplotlib.pyplot as plt
from itertools import combinations

def calcular_similaridade(disciplina1, disciplina2):
    """Calcula similaridade entre nomes de disciplinas usando RapidFuzz"""
    # Usando a razão de similaridade (token set ratio funciona bem para ordem diferente de palavras)
    return fuzz.token_set_ratio(disciplina1.nome.lower(), disciplina2.nome.lower()) / 100

class Grafo():
    def __init__(self, cursos):
        self.cores = cursos
        self.G = nx.Graph()

        # Adiciona todos os cursos ao grafo com atributos de unidade
        for curso in cursos:
            self.G.add_node(curso.nome, unidade=curso.unidade)

        # Dicionário para mapear tipo de disciplina para cor de aresta
        self.tipo_aresta_cor = {
            'obrigatoria': 'blue',
            'optativa_livre': 'green',
            'optativa_eletiva': 'red'
        }

        # Faz todas as combinações de curso para encontrar disciplinas em comum
        for curso1, curso2 in combinations(cursos, 2):
            contagem_por_tipo = {
                'obrigatoria': 0,
                'optativa_livre': 0,
                'optativa_eletiva': 0
            }
            
            # Compara todas as disciplinas entre os dois cursos
            for tipo in ['disc_obrigatorias', 'disc_op_livres', 'disc_op_eletivas']:
                for disc1 in getattr(curso1, tipo):
                    for disc2 in getattr(curso2, tipo):
                        similaridade = calcular_similaridade(disc1, disc2)
                        if similaridade >= 0.7:
                            tipo_simplificado = tipo.split('_')[-1]  # Pega "obrigatorias", "livres" ou "eletivas"
                            if tipo_simplificado == 'obrigatorias':
                                contagem_por_tipo['obrigatoria'] += 1
                            elif tipo_simplificado == 'livres':
                                contagem_por_tipo['optativa_livre'] += 1
                            else:
                                contagem_por_tipo['optativa_eletiva'] += 1
            
            # Adiciona arestas para cada tipo de disciplina
            for tipo, contagem in contagem_por_tipo.items():
                if contagem > 0:
                    self.G.add_edge(
                        curso1.nome, 
                        curso2.nome, 
                        weight=contagem,
                        tipo=tipo,
                        color=self.tipo_aresta_cor[tipo]
                    )

    def plotar_grafo(self, tamanho_fonte=8):
        """ Plota o grafo de cursos com cores personalizadas """
        plt.figure(figsize=(18, 12))
        
        # Escolhe o layout
        pos = nx.spring_layout(self.G, k=1.2, iterations=100)
    
        unidades = list({self.G.nodes[n]['unidade'] for n in self.G.nodes()})
        cmap = plt.cm.get_cmap('tab20', len(unidades))
        unidade_cores = {unidade: cmap(i) for i, unidade in enumerate(unidades)}
    
        # Cores dos nós
        node_colors = [unidade_cores[self.G.nodes[n]['unidade']] for n in self.G.nodes()]
        
        # Pega a cor de cada nó baseado na unidade
        node_colors = [unidade_cores.get(self.G.nodes[n]['unidade'], 'gray') for n in self.G.nodes()]
        
        # Desenha os nós
        nx.draw_networkx_nodes(
            self.G, 
            pos, 
            node_size=700,
            node_color=node_colors,
            edgecolors='black',
            linewidths=1
        )
        
        # Desenha as arestas agrupadas por tipo
        edges = self.G.edges(data=True)
        for tipo, cor in self.tipo_aresta_cor.items():
            edges_tipo = [(u, v) for (u, v, d) in edges if d.get('tipo') == tipo]
            widths_tipo = [d['weight'] for (u, v, d) in edges if d.get('tipo') == tipo]
            nx.draw_networkx_edges(
                self.G, 
                pos, 
                edgelist=edges_tipo,
                width=widths_tipo,
                edge_color=cor,
                alpha=0.7,
                label=f"{tipo.replace('_', ' ').title()}"
            )
        
        # Desenha os rótulos
        nx.draw_networkx_labels(self.G, pos, font_size=8)
        
        # Adiciona legendas para os pesos das arestas (opcional)
        edge_labels = {(u, v): f"{d['weight']}" for (u, v, d) in edges}
        nx.draw_networkx_edge_labels(
            self.G, 
            pos, 
            edge_labels=edge_labels, 
            font_size=6,
            bbox=dict(alpha=0.3)
        )
        
        # Adiciona legenda
        plt.legend(title="Tipo de Disciplina", loc='upper right')
        plt.title("Grafo de Similaridade entre Cursos (Cores por Unidade/Tipo de Disciplina)")
        plt.axis('off')
        plt.tight_layout()
        plt.show()