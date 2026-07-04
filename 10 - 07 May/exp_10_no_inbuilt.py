# Experiment 10: 07 May 2026
# To determine if the given two graphs have a Hamiltonian circuit and construct it not using NetworkX dedicated functions.
import networkx as nx
import matplotlib.pyplot as plt

def is_hamiltonian_and_circuit(G):
    nodes = list(G.nodes())
    n = len(nodes)
    
    if n < 3:
        return False,[]
        
    # Condition 1: if a graph has any vertex with degree < 2, Hamiltonian circuit is impossible
    for node in nodes:
        if G.degree(node) < 2:
            print(f"Condition check: Node '{node}' has degree {G.degree(node)} (< 2). Hamiltonian circuit is impossible.")
            return False,[]
            
    # condition 2: Dirac's theorem
    # If the degree of every vertex v is at least n/2, then the graph has a hamiltonin circuit
    dirac_satisfied = all(G.degree(node) >= n / 2.0 for node in nodes)
    if dirac_satisfied:
        print("Condition check: Dirac's theorem satisfied (all vertices have degree >= n/2). Graph is Hamiltonian.")
    else:
        print("Condition check: Dirac's theorem not satisfied (some vertices don't have degree >= n/2). Proceeding to backtracking algorithm.")
    
    # backtracking algo to find a single hamiltonian circuit
    def backtrack(path):
        if len(path) == n:
            # check if there is an edge from the last node to the first node to close the cycle
            if G.has_edge(path[-1], path[0]):
                return path +[path[0]]
            else:
                return None
                
        for neighbor in G.neighbors(path[-1]):
            if neighbor not in path:
                path.append(neighbor)
                result = backtrack(path)
                if result:
                    return result
                path.pop()
        return None

    # start the circuit from the first node
    start_node = nodes[0]
    circuit = backtrack([start_node])
    
    if circuit:
        return True, circuit
    else:
        return False,[]

print("Graph G1 Result:")
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

ax1_left.set_title("Original Graph", fontsize=14)
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
    ax1_right.set_title(f"Hamiltonian Circuit: {' -> '.join(circuit1)}", fontsize=14)
    nx.draw_networkx_nodes(G1, pos1, node_color='white', edgecolors='black', node_size=800, ax=ax1_right)
    nx.draw_networkx_labels(G1, pos1, font_color='black', font_size=12, font_family='sans-serif', ax=ax1_right)
    nx.draw_networkx_edges(G1, pos1, edgelist=solid_edges1, edge_color='lightgray', style='solid', width=2.0, ax=ax1_right)
    nx.draw_networkx_edges(G1, pos1, edgelist=[('E', 'D')], connectionstyle='arc3, rad=0.4', edge_color='lightgray', style='solid', width=2.0, ax=ax1_right, arrows=True, arrowstyle='-')
    
    circuit_edges = [(circuit1[i], circuit1[i+1]) for i in range(len(circuit1)-1)]
    nx.draw_networkx_edges(G1, pos1, edgelist=circuit_edges, edge_color='red', width=4.0, ax=ax1_right)
    
    ax1_right.set_xlim(-1, 5.5)
    ax1_right.set_ylim(-1.5, 4)
else:
    result_text = "Hamiltonian: No"
    ax1_right.text(0.5, 0.5, result_text, fontsize=16, ha='center', va='center', transform=ax1_right.transAxes)

plt.tight_layout()
plt.show()

print("\nGraph G2 Result:")
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

ax2_left.set_title("Original Graph", fontsize=14)
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

ax2_left.set_xlim(-1.5, 5.5)
ax2_left.set_ylim(-1.5, 4)
ax2_left.axis('off')

ax2_right.axis('off')
if is_ham2:
    ax2_right.set_title(f"Hamiltonian Circuit: {' -> '.join(circuit2)}", fontsize=14)
    nx.draw_networkx_nodes(G2, pos2, node_color='white', edgecolors='black', node_size=800, ax=ax2_right)
    nx.draw_networkx_labels(G2, pos2, font_color='black', font_size=12, font_family='sans-serif', ax=ax2_right)
    nx.draw_networkx_edges(G2, pos2, edgelist=solid_edges2, edge_color='lightgray', style='solid', width=2.0, ax=ax2_right)
    nx.draw_networkx_edges(G2, pos2, edgelist=[('E', 'D')], connectionstyle='arc3, rad=0.4', edge_color='lightgray', style='solid', width=2.0, ax=ax2_right, arrows=True, arrowstyle='-')
    nx.draw_networkx_edges(G2, pos2, edgelist=[('E', 'A')], connectionstyle='arc3, rad=-0.4', edge_color='lightgray', style='solid', width=2.0, ax=ax2_right, arrows=True, arrowstyle='-')
    
    circuit_edges = [(circuit2[i], circuit2[i+1]) for i in range(len(circuit2)-1)]
    nx.draw_networkx_edges(G2, pos2, edgelist=circuit_edges, edge_color='red', width=4.0, ax=ax2_right)
    
    ax2_right.set_xlim(-1.5, 5.5)
    ax2_right.set_ylim(-1.5, 4)
else:
    result_text = "Hamiltonian: No\n(Graph does not contain a Hamiltonian Circuit)"
    ax2_right.text(0.5, 0.5, result_text, fontsize=16, ha='center', va='center', transform=ax2_right.transAxes)

plt.tight_layout()
plt.show()