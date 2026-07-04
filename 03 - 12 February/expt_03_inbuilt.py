# 12 February 2026
# EXPERIMENT 03: SUBGRAPHS USING BUILT-IN NETWORKX FUNCTIONS
import networkx as nx
import matplotlib.pyplot as plt
import math

G = nx.Graph()

nodes_list =[0, 1, 2, 3, 4, 5, 6, 7]
for node in nodes_list:
    G.add_node(node)

pos = {}
r = 1

offset = math.pi / 8  
start_angle = (math.pi / 2) - offset
# node 0 top right
angle0 = start_angle
pos[0] = (r * math.cos(angle0), r * math.sin(angle0))
# node 1 right
angle1 = angle0 - (math.pi / 4)
pos[1] = (r * math.cos(angle1), r * math.sin(angle1))
# node 2 bottom right
angle2 = angle1 - (math.pi / 4)
pos[2] = (r * math.cos(angle2), r * math.sin(angle2))
# Node 3 bottom right lower one
angle3 = angle2 - (math.pi / 4)
pos[3] = (r * math.cos(angle3), r * math.sin(angle3))
# node 4 bottom left lower one
angle4 = angle3 - (math.pi / 4)
pos[4] = (r * math.cos(angle4), r * math.sin(angle4))
# Node 5 bottom left
angle5 = angle4 - (math.pi / 4)
pos[5] = (r * math.cos(angle5), r * math.sin(angle5))
# Node 6 left
angle6 = angle5 - (math.pi / 4)
pos[6] = (r * math.cos(angle6), r * math.sin(angle6))
# node 7 top left
angle7 = angle6 - (math.pi / 4)
pos[7] = (r * math.cos(angle7), r * math.sin(angle7))

# outer ring
G.add_edge(0, 1)
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 5)
G.add_edge(5, 6)
G.add_edge(6, 7)
G.add_edge(7, 0)

# inner ones but Skip-1
G.add_edge(0, 2)
G.add_edge(1, 3)
G.add_edge(2, 4)
G.add_edge(3, 5)
G.add_edge(4, 6)
G.add_edge(5, 7)
G.add_edge(6, 0)
G.add_edge(7, 1)

# diagonals
G.add_edge(0, 4)
G.add_edge(1, 5)
G.add_edge(2, 6)
G.add_edge(3, 7)

nodes_to_keep =[0, 1, 2, 4]
G_induced = G.subgraph(nodes_to_keep)

G_spanning = nx.minimum_spanning_tree(G)

G_deleted = G.copy()
G_deleted.remove_edges_from([(0, 4), (1, 5)])

outer_edges =[(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0)]
G_outer = G.edge_subgraph(outer_edges)

G_inter = G.copy()
G_inter.remove_edges_from(outer_edges)

plt.figure(figsize=(6, 6))
nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_size=500, edgecolors='black')
nx.draw_networkx_labels(G, pos, font_size=12)
nx.draw_networkx_edges(G, pos, edge_color='black', width=2)
plt.title("Canvas 1: Original Graph", fontsize=14, fontweight='bold')
plt.axis('off')
plt.show()

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle("Canvas 2: Subgraphs (Using Built-in NetworkX Functions)", fontsize=20)

ax = axes.flatten()

subgraphs_to_plot =[
    (G_induced, "Vertex Induced\n(G.subgraph)", "red"),
    (G_spanning, "Spanning Subgraph\n(nx.minimum_spanning_tree)", "green"),
    (G_deleted, "Edge Deleted\n(G.remove_edges_from)", "orange"),
    (G_outer, "Outer Link Subgraph\n(G.edge_subgraph)", "purple"),
    (G_inter, "Inter Link Subgraph\n(G.remove_edges_from)", "blue")
]

for i, (sub_g, title, color) in enumerate(subgraphs_to_plot):
    nx.draw_networkx_nodes(sub_g, pos, ax=ax[i], node_color='white', edgecolors=color, node_size=400)
    nx.draw_networkx_labels(sub_g, pos, ax=ax[i], font_size=10)
    nx.draw_networkx_edges(sub_g, pos, ax=ax[i], edge_color=color, width=2)
    
    ax[i].set_title(title, fontsize=12)
    ax[i].axis('off')

ax[5].axis('off')

plt.tight_layout()
plt.show()