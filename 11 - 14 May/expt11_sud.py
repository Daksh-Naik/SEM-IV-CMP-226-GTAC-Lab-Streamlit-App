import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
nodes = list(range(1, 17))
G.add_nodes_from(nodes)
pos = {1: (0, 3), 2: (1, 3), 3: (2, 3), 4: (3, 3), 
       5: (0, 2), 6: (1, 2), 7: (2, 2), 8: (3, 2), 
       9: (0, 1), 10: (1, 1), 11: (2, 1), 12: (3, 1), 
       13: (0, 0), 14: (1, 0), 15: (2, 0), 16: (3, 0)}

edges = [
    (3, 1), (3, 2), (3, 4),         # Row
    (3, 7), (3, 11), (3, 15),       # Column
    (3, 8),                         # Block
    
    (9, 1), (9, 5), (9, 13),        # Column
    (9, 10), (9, 11), (9, 12),      # Row
    (9, 14),                        # Block
    
    (16, 4), (16, 8), (16, 12),     # Column
    (16, 13), (16, 14), (16, 15),   # Row
    (16, 11)                        # Block
]

G.add_edges_from(edges)
special_labels = {3: '1', 9: '3', 16: '3'}
color_map = []
for node in G.nodes():
    if node in special_labels:
        color_map.append('skyblue')
    else:
        color_map.append('lightgray')

labels = {node: special_labels.get(node, str(node)) for node in G.nodes()}

fig, axes = plt.subplots(1, 2, figsize=(14, 7))

nx.draw_networkx_nodes(G, pos, ax=axes[0], node_color=color_map, node_size=800, edgecolors='black')

curved_edges = [(3, 1), (3, 11), (3, 15), (9, 11), (9, 12), (9,1), (16,14), (16,13), (16,8), (16,4)]
straight_edges = [edge for edge in G.edges() if edge not in curved_edges and (edge[1], edge[0]) not in curved_edges]

nx.draw_networkx_edges(G, pos, ax=axes[0], edgelist=straight_edges, width=2.0, edge_color='black')
nx.draw_networkx_edges(G, pos, ax=axes[0], edgelist=curved_edges, connectionstyle='arc3, rad=-0.25', edge_color='black', style='solid', width=2.0, arrows=True, arrowstyle='-')

label_colors = {'blue': 'white', 'green': 'white', 'lightgray': 'black', 'skyblue': 'black'}

for node, color in zip(G.nodes(), color_map):
    nx.draw_networkx_labels(G, pos, ax=axes[0], labels={node: labels[node]}, font_color=label_colors[color], font_weight='bold')

axes[0].set_title("Given Sudoku Graph (Initial State)", fontsize=14, fontweight='bold')
axes[0].axis('off')

vertex_set = [1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15]
colors_set = ['Blue', 'Red', 'Green', 'Black']

G_full = nx.Graph()
G_full.add_nodes_from(nodes)

full_edges = [
    # Row 1 conflicts
    (1,2), (1,3), (1,4), (2,3), (2,4), (3,4),
    # Row 2 conflicts
    (5,6), (5,7), (5,8), (6,7), (6,8), (7,8),
    # Row 3 conflicts
    (9,10), (9,11), (9,12), (10,11), (10,12), (11,12),
    # Row 4 conflicts
    (13,14), (13,15), (13,16), (14,15), (14,16), (15,16),

    # Column 1 conflicts
    (1,5), (1,9), (1,13), (5,9), (5,13), (9,13),
    # Column 2 conflicts
    (2,6), (2,10), (2,14), (6,10), (6,14), (10,14),
    # Column 3 conflicts
    (3,7), (3,11), (3,15), (7,11), (7,15), (11,15),
    # Column 4 conflicts
    (4,8), (4,12), (4,16), (8,12), (8,16), (12,16),

    # 2x2 block conflicts (diagonals that aren't already covered by rows/cols)
    (1,6), (2,5),       # top-left bblock
    (3,8), (4,7),       # top-right block
    (9,14), (10,13),    # botom-left block
    (11,16), (12,15)    # bottom-right block
]

G_full.add_edges_from(full_edges)

strategy_order = [3, 1, 2, 4, 5, 8, 7, 6, 12, 10, 9, 11, 14, 15, 16, 13]

coloring = nx.coloring.greedy_color(G_full, strategy=lambda G, colors: strategy_order)

color_mapping = {0: 'Blue', 1: 'Red', 2: 'Green', 3: 'Black'}
solved_colors = {node: color_mapping[c] for node, c in coloring.items()}

rhs_node_colors = []
for node in G.nodes():
    c = solved_colors[node]
    if c == 'Blue': rhs_node_colors.append('blue')
    elif c == 'Red': rhs_node_colors.append('red')
    elif c == 'Green': rhs_node_colors.append('green')
    elif c == 'Black': rhs_node_colors.append('black')

rhs_value_mapping = {'Blue': '1', 'Red': '2', 'Green': '3', 'Black': '4'}
rhs_labels = {node: rhs_value_mapping[solved_colors[node]] for node in G.nodes()}
rhs_label_colors = {'blue': 'white', 'red': 'white', 'green': 'white', 'black': 'white'}

rhs_black_edges = straight_edges + curved_edges
rhs_black_edges_set = set(rhs_black_edges) | {(v, u) for u, v in rhs_black_edges}
rhs_gray_edges = [edge for edge in G_full.edges() if edge not in rhs_black_edges_set]

desired_gray_curves = [
    (10, 2), (11, 9),        
    (1, 3), (1, 4), (2, 4),             # Row 1 jumps
    (1, 9), (1, 13), (5, 13),           # Column 1 jumps
    (2, 14),
    (5, 7), (5, 8), (6, 8), (6, 14), (7, 15),
    (15, 13), (8, 16),
    (12, 4), (10, 12), 
]

gray_curved_edges = []
for u, v in desired_gray_curves:
    if (u, v) in rhs_gray_edges:
        gray_curved_edges.append((u, v))
    elif (v, u) in rhs_gray_edges:
        gray_curved_edges.append((v, u))

gray_straight_edges = [edge for edge in rhs_gray_edges if edge not in gray_curved_edges and (edge[1], edge[0]) not in gray_curved_edges]

nx.draw_networkx_nodes(G, pos, ax=axes[1], node_color=rhs_node_colors, node_size=800, edgecolors='black')

nx.draw_networkx_edges(G_full, pos, ax=axes[1], edgelist=gray_straight_edges, width=1.0, edge_color='gray')

nx.draw_networkx_edges(G_full, pos, ax=axes[1], edgelist=gray_curved_edges, 
                       connectionstyle='arc3, rad=-0.25', edge_color='gray', 
                       style='solid', width=1.0, arrows=True, arrowstyle='-')


nx.draw_networkx_edges(G, pos, ax=axes[1], edgelist=straight_edges, width=2.0, edge_color='black')
nx.draw_networkx_edges(G, pos, ax=axes[1], edgelist=curved_edges, 
                       connectionstyle='arc3, rad=-0.25', edge_color='black', 
                       style='solid', width=2.0, arrows=True, arrowstyle='-')

for node, color in zip(G.nodes(), rhs_node_colors):
    nx.draw_networkx_labels(G, pos, ax=axes[1], labels={node: rhs_labels[node]}, font_color=rhs_label_colors[color], font_weight='bold', font_size=10)

axes[1].set_title("Solved Graph via Greedy Algorithm", fontsize=14, fontweight='bold', color='black')
axes[1].axis('off')

plt.tight_layout()
plt.show()