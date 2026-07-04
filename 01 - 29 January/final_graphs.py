# 29 January - First Lab Program
import networkx as nx
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10, 10))

#___________________________________________________________________
# K5 Graph
G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5])
ax1 = fig.add_subplot(2, 2, 1)

G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(1, 4)
G.add_edge(1, 5)

G.add_edge(2, 3)
G.add_edge(2, 4)
G.add_edge(2, 5)

G.add_edge(3, 4)
G.add_edge(3, 5)

G.add_edge(4, 5)

pos = nx.circular_layout(G) 

nx.draw(G, pos, ax=ax1, with_labels=True, node_color='lightgreen', font_weight='bold')
ax1.set_title("Complete Graph - K5")

#___________________________________________________________________
# C5 Graph

C5 = nx.Graph()
C5.add_nodes_from([0, 1, 2, 3, 4])
ax2 = fig.add_subplot(2, 2, 2)

C5.add_edge(0, 1)
C5.add_edge(1, 2)
C5.add_edge(2, 3)
C5.add_edge(3, 4)
C5.add_edge(4, 0)

pos_c5 = nx.circular_layout(C5)
nx.draw(C5, pos_c5, ax=ax2, with_labels=True, node_color='lightblue', font_weight='bold')
ax2.set_title("Cycle Graph - C5")

#___________________________________________________________________
# P5 (Path Graph)

P5 = nx.Graph()
P5.add_nodes_from([1, 2, 3, 4, 5])
ax3 = fig.add_subplot(2, 2, 3)

P5.add_edge(1, 2)
P5.add_edge(2, 3)
P5.add_edge(3, 4)
P5.add_edge(4, 5)

pos_p5 = nx.spring_layout(P5)
nx.draw(P5, pos_p5, ax = ax3, with_labels = True, node_color = 'orange', font_weight = 'bold')
ax3.set_title("Path Graph - P5")


#___________________________________________________________________
# K2,3 Bipartite Graph

K23 = nx.Graph()
K23.add_nodes_from([1, 2, 3, 4, 5])
ax4 = fig.add_subplot(2, 2, 4)

K23.add_edge(1, 3)
K23.add_edge(1, 4)
K23.add_edge(1, 5)
K23.add_edge(2, 3)
K23.add_edge(2, 4)
K23.add_edge(2, 5)

pos_k23 = nx.bipartite_layout(K23, [1, 2], align='horizontal')
for node in pos_k23:
    pos_k23[node][1] = -pos_k23[node][1]
nx.draw(K23, pos_k23, ax=ax4, with_labels=True, node_color='aqua', font_weight='bold')
ax4.set_title("Bipartite Graph - K2,3")

plt.tight_layout()
plt.suptitle("EXP 01 - Types of Graphs")
plt.show()