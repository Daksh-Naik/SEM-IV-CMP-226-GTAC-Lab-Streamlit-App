# Experiment 10: 07 May 2026
# To determine if the given two graphs have a Hamiltonian circuit and construct it using NetworkX dedicated functions.

import networkx as nx
import matplotlib.pyplot as plt

def is_hamiltonian_and_circuit(G):
    n = len(G.nodes())
    if n < 3:
        return False, None
    
    nodes = list(G.nodes())
    path = [nodes[0]]
    visited = set(path)
    
    def backtrack():
        if len(path) == n:
            if G.has_edge(path[-1], path[0]):
                return True
            return False
        
        for neighbor in G.neighbors(path[-1]):
            if neighbor not in visited:
                path.append(neighbor)
                visited.add(neighbor)
                if backtrack():
                    return True
                path.pop()
                visited.remove(neighbor)
        return False
    
    if backtrack():
        circuit = path + [path[0]]
        return True, circuit
    return False, None

G1 = nx.Graph()
G1.add_nodes_from(['A', 'B', 'E', 'D', 'C'])

pos1 = {
    'A': (0, 3),
    'B': (2.5, 3),
    'E': (0, 0),
    'D': (2.5, 0),
    'C': (4.5, 0)
}

solid_edges1 =[('A', 'B'), ('A', 'E'), ('E', 'D'), ('D', 'C'), ('A', 'D')]

G1.add_edges_from(solid_edges1)

is_ham1, circuit1 = is_hamiltonian_and_circuit(G1)

fig1, (ax1_left, ax1_right) = plt.subplots(1, 2, figsize=(14, 6))
fig1.suptitle("Graph G1", fontweight='bold', fontsize=16)

nx.draw_networkx_nodes(G1, pos1, node_color='white', edgecolors='black', node_size=800, ax=ax1_left)
nx.draw_networkx_labels(G1, pos1, font_color='black', font_size=12, font_family='sans-serif', ax=ax1_left)

nx.draw_networkx_edges(G1, pos1, edgelist=solid_edges1, edge_color='black', style='solid', width=2.0, ax=ax1_left)

nx.draw_networkx_edges(
    G1, pos1, 
    edgelist=[('E', 'D')], 
    connectionstyle='arc3, rad=0.4', 
    edge_color='black', 
    style='solid', 
    width=2.0, 
    ax=ax1_left,
    arrows=True,
    arrowstyle='-'
)

edge_labels1 = {
    ('A', 'B'): 'e1', ('A', 'E'): 'e2', ('A', 'D'): 'e3', 
    ('E', 'D'): 'e4', ('D', 'C'): 'e5'
}
nx.draw_networkx_edge_labels(G1, pos1, edge_labels=edge_labels1, font_color='black', font_size=12, ax=ax1_left)

ax1_left.text(1.25, -0.6, 'e6', fontsize=12, color='black',
         bbox=dict(facecolor='white', edgecolor='none', pad=1.0), 
         horizontalalignment='center', verticalalignment='center')

ax1_left.set_xlim(-1, 5.5)
ax1_left.set_ylim(-1.5, 4)
ax1_left.axis('off')

ax1_right.axis('off')
if is_ham1:
    result_text = f"Hamiltonian: Yes\nCircuit: {' -> '.join(circuit1)}"
else:
    result_text = "Hamiltonian: No"
ax1_right.text(0.5, 0.5, result_text, fontsize=14, ha='center', va='center', transform=ax1_right.transAxes)

plt.tight_layout()
plt.show()

# GRAPH 2 (G2)
G2 = nx.Graph()
G2.add_nodes_from(['A', 'B', 'E', 'D', 'C'])

pos2 = {
    'A': (0, 3),
    'B': (2.5, 3),
    'E': (0, 0),
    'D': (2.5, 0),
    'C': (4.5, 0)
}

solid_edges2 =[('A', 'B'), ('A', 'E'), ('E', 'D'), ('D', 'C'), ('A', 'D'), ('B', 'C')]

G2.add_edges_from(solid_edges2)

is_ham2, circuit2 = is_hamiltonian_and_circuit(G2)

fig2, (ax2_left, ax2_right) = plt.subplots(1, 2, figsize=(14, 6))
fig2.suptitle("Graph G2", fontweight='bold', fontsize=16)

nx.draw_networkx_nodes(G2, pos2, node_color='white', edgecolors='black', node_size=800, ax=ax2_left)
nx.draw_networkx_labels(G2, pos2, font_color='black', font_size=12, font_family='sans-serif', ax=ax2_left)

nx.draw_networkx_edges(G2, pos2, edgelist=solid_edges2, edge_color='black', style='solid', width=2.0, ax=ax2_left)

nx.draw_networkx_edges(
    G2, pos2, 
    edgelist=[('E', 'D')], 
    connectionstyle='arc3, rad=0.4', 
    edge_color='black', 
    style='solid', 
    width=2.0, 
    ax=ax2_left,
    arrows=True,
    arrowstyle='-'
)

nx.draw_networkx_edges(
    G2, pos2,
    edgelist=[('E', 'A')],
    connectionstyle='arc3, rad=-0.4',
    edge_color='black',
    style='solid',
    width=2.0,
    ax=ax2_left,
    arrows=True,
    arrowstyle='-'
)

edge_labels2 = {
    ('A', 'B'): 'e1', ('A', 'E'): 'e2', ('A', 'D'): 'e3', 
    ('E', 'D'): 'e4', ('D', 'C'): 'e5', ('B', 'C'): 'e8'
}
nx.draw_networkx_edge_labels(G2, pos2, edge_labels=edge_labels2, font_color='black', font_size=12, ax=ax2_left)

ax2_left.text(1.25, -0.6, 'e6', fontsize=12, color='black',
         bbox=dict(facecolor='white', edgecolor='none', pad=1.0),
         horizontalalignment='center', verticalalignment='center')

ax2_left.text(-0.7, 1.5, 'e7', fontsize=12, color='black',
         bbox=dict(facecolor='white', edgecolor='none', pad=1.0),
         horizontalalignment='center', verticalalignment='center')

if is_ham2:
    circuit_edges = [(circuit2[i], circuit2[i+1]) for i in range(len(circuit2)-1)]
    nx.draw_networkx_edges(G2, pos2, edgelist=circuit_edges, edge_color='red', width=4.0, ax=ax2_left)

ax2_left.set_xlim(-1.5, 5.5)
ax2_left.set_ylim(-1.5, 4)
ax2_left.axis('off')

ax2_right.axis('off')
if is_ham2:
    result_text = f"Hamiltonian: Yes\nCircuit: {' -> '.join(circuit2)}"
else:
    result_text = "Hamiltonian: No"
ax2_right.text(0.5, 0.5, result_text, fontsize=14, ha='center', va='center', transform=ax2_right.transAxes)

plt.tight_layout()
plt.show()