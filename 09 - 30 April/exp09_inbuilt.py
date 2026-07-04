# Experiment 09: 30 April 2026 (using NetworkX)
# To implement an algorithm that checks for the existence of an Euler circuit, 
# and construct the circuit that traverses every edge of the graph exactly once.

import networkx as nx
import matplotlib.pyplot as plt

# PC crashed oof
fig, axs = plt.subplots(2, 2, figsize=(14, 10), gridspec_kw={'height_ratios': [2.5, 1]})
fig.suptitle("Euler Circuit Analysis (30/4/26)", fontweight='bold', fontsize=18)

ax1 = axs[0, 0]
ax2 = axs[0, 1]
ax_res1 = axs[1, 0]
ax_res2 = axs[1, 1]

G1 = nx.MultiGraph()
G1.add_nodes_from(['A', 'B', 'E', 'D', 'C'])

pos1 = {'A': (0, 3), 'B': (2.5, 3), 'E': (0, 0), 'D': (2.5, 0), 'C': (4.5, 0)}

solid_edges1 = [('A', 'B'), ('A', 'E'), ('E', 'D'), ('D', 'C'), ('A', 'D')]
G1.add_edges_from(solid_edges1)
G1.add_edge('E', 'D') 

nx.draw_networkx_nodes(G1, pos1, node_color='white', edgecolors='black', node_size=800, ax=ax1)
nx.draw_networkx_labels(G1, pos1, font_color='black', font_size=12, font_family='sans-serif', ax=ax1)
nx.draw_networkx_edges(G1, pos1, edgelist=solid_edges1, edge_color='black', style='solid', width=2.0, ax=ax1)

nx.draw_networkx_edges(
    G1, pos1, edgelist=[('E', 'D')], connectionstyle='arc3, rad=0.4', 
    edge_color='black', style='solid', width=2.0, ax=ax1, arrows=True, arrowstyle='-'
)

edge_labels1 = {('A', 'B'): 'e1', ('A', 'E'): 'e2', ('A', 'D'): 'e3', ('E', 'D'): 'e4', ('D', 'C'): 'e5'}
nx.draw_networkx_edge_labels(G1, pos1, edge_labels=edge_labels1, font_color='black', font_size=12, ax=ax1)

ax1.text(1.25, -0.6, 'e6', fontsize=12, color='black',
         bbox=dict(facecolor='white', edgecolor='none', pad=1.0), ha='center', va='center')

ax1.set_title("Graph 1", fontweight='bold', fontsize=14)
ax1.set_xlim(-1, 5.5)
ax1.set_ylim(-1.5, 4)
ax1.axis('off')

G2 = nx.MultiGraph()
G2.add_nodes_from(['A', 'B', 'E', 'D', 'C'])

pos2 = {'A': (0, 3), 'B': (2.5, 3), 'E': (0, 0), 'D': (2.5, 0), 'C': (4.5, 0)}

solid_edges2 = [('A', 'B'), ('A', 'E'), ('E', 'D'), ('D', 'C'), ('A', 'D'), ('B', 'C')]
G2.add_edges_from(solid_edges2)
G2.add_edge('E', 'D') 
G2.add_edge('E', 'A') 

nx.draw_networkx_nodes(G2, pos2, node_color='white', edgecolors='black', node_size=800, ax=ax2)
nx.draw_networkx_labels(G2, pos2, font_color='black', font_size=12, font_family='sans-serif', ax=ax2)
nx.draw_networkx_edges(G2, pos2, edgelist=solid_edges2, edge_color='black', style='solid', width=2.0, ax=ax2)

nx.draw_networkx_edges(
    G2, pos2, edgelist=[('E', 'D')], connectionstyle='arc3, rad=0.4', 
    edge_color='black', style='solid', width=2.0, ax=ax2, arrows=True, arrowstyle='-'
)
nx.draw_networkx_edges(
    G2, pos2, edgelist=[('E', 'A')], connectionstyle='arc3, rad=-0.4',
    edge_color='black', style='solid', width=2.0, ax=ax2, arrows=True, arrowstyle='-'
)

edge_labels2 = {('A', 'B'): 'e1', ('A', 'E'): 'e2', ('A', 'D'): 'e3', ('E', 'D'): 'e4', ('D', 'C'): 'e5', ('B', 'C'): 'e8'}
nx.draw_networkx_edge_labels(G2, pos2, edge_labels=edge_labels2, font_color='black', font_size=12, ax=ax2)

ax2.text(1.25, -0.6, 'e6', fontsize=12, color='black', bbox=dict(facecolor='white', edgecolor='none', pad=1.0), ha='center', va='center')
ax2.text(-0.7, 1.5, 'e7', fontsize=12, color='black', bbox=dict(facecolor='white', edgecolor='none', pad=1.0), ha='center', va='center')

ax2.set_title("Graph 2", fontweight='bold', fontsize=14)
ax2.set_xlim(-1.5, 5.5)
ax2.set_ylim(-1.5, 4)
ax2.axis('off')

is_eulerian_G1 = nx.is_eulerian(G1)
res_text1 = f"Graph 1 Analysis\n\nEulerian Circuit Exists: {is_eulerian_G1}\n\n"

if is_eulerian_G1:
    circuit1 = list(nx.eulerian_circuit(G1))
    path1 = " \u2192 ".join([u for u, v in circuit1] + [circuit1[-1][1]])
    res_text1 += f"Circuit Path:\n{path1}"
else:
    res_text1 += "No Euler circuit exists because not all\nvertices have an even degree."

ax_res1.text(0.5, 0.5, res_text1, fontsize=14, ha='center', va='center')
ax_res1.axis('off')

is_eulerian_G2 = nx.is_eulerian(G2)
res_text2 = f"Graph 2 Analysis\n\nEulerian Circuit Exists: {is_eulerian_G2}\n\n"

if is_eulerian_G2:
    circuit2 = list(nx.eulerian_circuit(G2))
    path2 = " \u2192 ".join([u for u, v in circuit2] + [circuit2[-1][1]])
    res_text2 += f"Circuit Path:\n{path2}"
else:
    res_text2 += "No Euler circuit exists because not all\nvertices have an even degree."

ax_res2.text(0.5, 0.5, res_text2, fontsize=14, ha='center', va='center')
ax_res2.axis('off')

plt.tight_layout()
plt.show()