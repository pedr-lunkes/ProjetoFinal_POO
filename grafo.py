# Grupo composto por:
# Pedro Henrique de Sousa Prestes	15507819
# Pedro Henrique Perez Dias		15484075
# Pedro Lunkes Villela			15484287

import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from itertools import combinations
class Grafo:
    def __init__(self, cursos):
        self.G = nx.Graph()

        # Dicionário para mapear curso para seu ID único
        self.curso_para_id = {}
        
        # Adiciona nós com ID único (unidade + nome)
        for curso in cursos:
            node_id = f"{curso.unidade} - {curso.nome}"
            self.curso_para_id[(curso.unidade, curso.nome)] = node_id  # Chave única: (unidade, nome)
            self.G.add_node(node_id, unidade=curso.unidade, nome_curso=curso.nome)

        self.tipo_prioridade = ['obrigatoria', 'optativa_livre', 'optativa_eletiva']
        self.tipo_aresta_cor = {
            'obrigatoria': 'blue',
            'optativa_livre': 'green',
            'optativa_eletiva': 'red'
        }

        for curso1, curso2 in combinations(cursos, 2):
            contagem_por_tipo = {
                'obrigatoria': 0,
                'optativa_livre': 0,
                'optativa_eletiva': 0
            }


            # Calcula similaridades por tipo
            for tipo in ['disc_obrigatorias', 'disc_op_livres', 'disc_op_eletivas']:
                for disc1 in getattr(curso1, tipo):
                    for disc2 in getattr(curso2, tipo):
                        if disc1.nome == disc2.nome:
                            tipo_simplificado = tipo.split('_')[-1]
                            if tipo_simplificado == 'obrigatorias':
                                contagem_por_tipo['obrigatoria'] += 1
                            elif tipo_simplificado == 'livres':
                                contagem_por_tipo['optativa_livre'] += 1
                            else:
                                contagem_por_tipo['optativa_eletiva'] += 1

            # Adiciona aresta para cada tipo com similaridade
            total_curso1 = len(curso1.disc_obrigatorias) + len(curso1.disc_op_livres) + len(curso1.disc_op_eletivas)
            total_curso2 = len(curso2.disc_obrigatorias) + len(curso2.disc_op_livres) + len(curso2.disc_op_eletivas)

            for tipo in self.tipo_prioridade:
                if contagem_por_tipo[tipo] > 0:
                    proporcao = sum(contagem_por_tipo.values()) / max(total_curso1, total_curso2)
                    
                    # Usa os IDs únicos dos cursos
                    node1 = self.curso_para_id[(curso1.unidade, curso1.nome)]
                    node2 = self.curso_para_id[(curso2.unidade, curso2.nome)]
                    
                    self.G.add_edge(
                        node1, 
                        node2, 
                        weight=round(proporcao * 10, 1),
                        tipo=tipo,
                        color=self.tipo_aresta_cor[tipo]
                    )
                    break

    def plotar_grafo(self):
        plt.figure(figsize=(18, 12))
        pos = nx.kamada_kawai_layout(self.G)

        # Cores dos nós por unidade
        unidades = list({self.G.nodes[n]['unidade'] for n in self.G.nodes()})
        cmap = plt.cm.get_cmap('tab20', len(unidades))
        unidade_cores = {u: cmap(i) for i, u in enumerate(unidades)}
        node_colors = [unidade_cores[self.G.nodes[n]['unidade']] for n in self.G.nodes()]

        # Desenha nós
        nx.draw_networkx_nodes(
            self.G, pos, node_color=node_colors, node_size=700,
            edgecolors='black', linewidths=1
        )

        # Rótulos dos nós (mostra apenas o nome do curso, sem a unidade)
        labels = {n: self.G.nodes[n]['nome_curso'] for n in self.G.nodes()}
        nx.draw_networkx_labels(self.G, pos, labels, font_size=8)

        # Desenha arestas por tipo
        edges = self.G.edges(data=True)
        for tipo, cor in self.tipo_aresta_cor.items():
            edgelist = [(u, v) for u, v, d in edges if d['tipo'] == tipo]
            widths = [d['weight'] for u, v, d in edges if d['tipo'] == tipo]
            nx.draw_networkx_edges(
                self.G, pos, edgelist=edgelist,
                edge_color=cor, width=widths,
                alpha=0.7, label=tipo.replace('_', ' ').title()
            )

        # Legenda das unidades
        legenda_unidades = plt.legend(
            handles=[
                plt.Line2D([0], [0], marker='o', color='w',
                        markerfacecolor=cor, markersize=10, label=unidade)
                for unidade, cor in unidade_cores.items()
            ],
            title="Unidades", loc='upper left'
        )
        plt.gca().add_artist(legenda_unidades)

        # Legenda dos tipos de aresta
        plt.legend(
            handles=[
                plt.Line2D([0], [0], color=cor, lw=3, label=tipo.replace('_', ' ').title())
                for tipo, cor in self.tipo_aresta_cor.items()
            ],
            title="Tipo de Disciplina", loc='lower right', bbox_to_anchor=(1, 0)
        )

        plt.title("Grafo de Similaridade entre Cursos\n(Tamanho da aresta = Proporção de disciplinas similares)")
        plt.axis('off')
        plt.tight_layout()
        plt.show()