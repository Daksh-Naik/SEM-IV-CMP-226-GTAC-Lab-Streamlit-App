# 29 January - Experiment 1 - Not NetworkX Python Program
import matplotlib.pyplot as plt
import networkx as nx

def add_complete_graph_edges(graph: nx.Graph, num_nodes: int) -> None:
    for i in range(num_nodes):
        for j in range(num_nodes):
            # this here is to prevent a node to connect to itself (no self-loops)
            if i != j:
                graph.add_edge(i, j)

def add_cycle_graph_edges(graph: nx.Graph, num_nodes: int) -> None:
    for i in range(num_nodes - 1):
        graph.add_edge(i, i + 1)
        
    # To close the cycle without using the modulo operator (%), 
    # we explicitly connect the very last node back to the first node (0).
    graph.add_edge(num_nodes - 1, 0)

def add_path_graph_edges(graph: nx.Graph, num_nodes: int) -> None:
    for i in range(num_nodes - 1):
        graph.add_edge(i, i + 1)

def add_bipartite_graph_edges(graph: nx.Graph, set_a_size: int, set_b_size: int) -> None:
    """
    Set A contains nodes from 0 to (set_a_size - 1).
    Set B contains nodes from set_a_size to (set_a_size + set_b_size - 1).
    """
    for i in range(set_a_size):
        for j in range(set_b_size):
            # calculate the exact ID of the node in Set B, then the next line connects it
            node_in_b: int = set_a_size + j
            graph.add_edge(i, node_in_b)


#___________________________________________________________________
fig = plt.figure(figsize=(10, 10))

ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4)

#___________________________________________________________________
# K5 Graph
K5 = nx.Graph()
K5.add_nodes_from([0, 1, 2, 3, 4])
add_complete_graph_edges(graph=K5, num_nodes=5)

# placing nodes in a pentagon like shape without trigonometry
pos_k5: dict[int, tuple[float, float]] = {}
pos_k5[0] = (0.0, 2.0)   # Top center
pos_k5[1] = (2.0, 1.0)   # Top right
pos_k5[2] = (1.0, -1.0)  # Bottom right
pos_k5[3] = (-1.0, -1.0) # Bottom left
pos_k5[4] = (-2.0, 1.0)  # Top left

nx.draw(K5, pos_k5, ax=ax1, 
        with_labels=True, node_color='lightgreen', font_weight='bold')
ax1.set_title("Complete Graph - K5")

#___________________________________________________________________
# C5 Graph
C5 = nx.Graph()
C5.add_nodes_from([0, 1, 2, 3, 4])
add_cycle_graph_edges(graph=C5, num_nodes=5)

# reused K5 lines to show the cycle clearly
pos_c5: dict[int, tuple[float, float]] = {}
pos_c5[0] = (0.0, 2.0)
pos_c5[1] = (2.0, 1.0)
pos_c5[2] = (1.0, -1.0)
pos_c5[3] = (-1.0, -1.0)
pos_c5[4] = (-2.0, 1.0)

nx.draw(C5, pos_c5, ax=ax2, 
        with_labels=True, node_color='lightblue', font_weight='bold')
ax2.set_title("Cycle Graph - C5")

#___________________________________________________________________
# P5 Graph
P5 = nx.Graph()
P5.add_nodes_from([0, 1, 2, 3, 4])
add_path_graph_edges(graph=P5, num_nodes=5)

# straight line coords
pos_p5: dict[int, tuple[float, float]] = {}
pos_p5[0] = (0.0, 0.0)
pos_p5[1] = (1.0, 0.0)
pos_p5[2] = (2.0, 0.0)
pos_p5[3] = (3.0, 0.0)
pos_p5[4] = (4.0, 0.0)

nx.draw(P5, pos_p5, ax=ax3, 
        with_labels=True, node_color='orange', font_weight='bold')
ax3.set_title("Path Graph - P5")

#___________________________________________________________________
# K2,3 Bipartite Graph
K23 = nx.Graph()
K23.add_nodes_from([0, 1, 2, 3, 4])
add_bipartite_graph_edges(graph=K23, set_a_size=2, set_b_size=3)

pos_k23: dict[int, tuple[float, float]] = {}

# Set A
pos_k23[0] = (0.0, 1.0)
pos_k23[1] = (0.0, -1.0)

# Set B
pos_k23[2] = (2.0, 2.0)
pos_k23[3] = (2.0, 0.0)
pos_k23[4] = (2.0, -2.0)

nx.draw(K23, pos_k23, ax=ax4, with_labels=True, node_color='pink', font_weight='bold')
ax4.set_title("Bipartite Graph - K2,3")

plt.tight_layout()
plt.suptitle("Lab Session 1 Graphs", y=1.02, fontsize=14, fontweight='bold')
plt.show()