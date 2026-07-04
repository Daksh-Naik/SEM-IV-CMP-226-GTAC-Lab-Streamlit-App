import networkx as nx
import matplotlib.pyplot as plt

def get_sort_key(node_info: dict) -> tuple:
    return (-node_info['deg'], node_info['node'])

def get_user_sequence() -> list[int]:
    while True:
        user_input = input("Enter a degree sequence separated by spaces: ").replace(',', ' ')
        parts = user_input.split()
        sequence = []
        is_valid = True

        for part in parts:
            try:
                sequence.append(int(part))
            except ValueError:
                print("Error: Invalid input. Please enter only integers.")
                is_valid = False
                break

        if is_valid and len(sequence) > 0:
            return sequence
        elif len(sequence) == 0:
            print("Error: Sequence cannot be empty. Try again.")


def realize_and_draw(deg_seq: list[int], show: bool = True) -> tuple[bool, nx.Graph]:
    seq = list(deg_seq)
    n = len(seq)

    for d in seq:
        if d < 0:
            raise ValueError("Degrees must be non-negative")

    if sum(seq) % 2 == 1:
        print("Sum of degrees is odd -> sequence cannot be graphical")

    nodes = list(range(1, n + 1))
    residual = [{'node': nodes[i], 'deg': seq[i]} for i in range(n)]

    G = nx.Graph()
    G.add_nodes_from(nodes)

    colors = ['red', 'yellow', 'green', 'blue', 'purple', 'orange', 'cyan', 'magenta', 'brown', 'gray']
    pos = nx.circular_layout(nodes)

    cols = 3
    max_plots = n + 2
    rows = (max_plots + cols - 1) // cols
    fig = plt.figure(figsize=(20, 12 * rows))
    plot_idx = [1]

    def draw_current(iteration: int, node_color: str):
        ax = fig.add_subplot(rows, cols, plot_idx[0])
        plot_idx[0] += 1

        labels = {r['node']: f"{r['node']}\n({r['deg']})" for r in residual}
        ax.set_axis_off()
        edge_list = list(G.edges())
        edge_colors = [
            colors[(attr.get('iter', 1) - 1) % len(colors)] if attr.get('iter', 0) > 0 else 'black'
            for _, _, attr in G.edges(data=True)
        ]
        ax.margins(0.1)
        nx.draw_networkx_nodes(G, pos=pos, node_color=node_color, node_size=700, ax=ax)
        nx.draw_networkx_labels(G, pos=pos, labels=labels, ax=ax)
        if edge_list:
            nx.draw_networkx_edges(G, pos=pos, edgelist=edge_list, edge_color=edge_colors, width=2, ax=ax)

        ax.set_title(f"Iteration {iteration}", fontsize=10, pad=0)

    iteration = 0
    draw_current(iteration, 'lightgray')

    while True:
        residual.sort(key=get_sort_key)

        if residual[0]['deg'] == 0:
            print("All residual degrees are zero. Sequence is graphical.")
            draw_current(iteration, 'lightblue')
            break

        top = residual[0]
        d, u = top['deg'], top['node']
        iteration += 1

        if d > len(residual) - 1:
            print(f"Degree {d} is too large for remaining nodes -> not graphical.")
            draw_current(iteration, 'salmon')
            plt.tight_layout()
            if show:
                plt.show()
            return False, G

        for i in range(1, d + 1):
            v_info = residual[i]
            v_info['deg'] -= 1
            G.add_edge(u, v_info['node'], iter=iteration)

            if v_info['deg'] < 0:
                print("Negative residual degree encountered -> not graphical.")
                draw_current(iteration, 'salmon')
                plt.tight_layout()
                if show:
                    plt.show()
                return False, G

        top['deg'] = 0
        draw_current(iteration, 'lightgreen')

    plt.tight_layout()
    if show:
        plt.show()
    return True, G

if __name__ == '__main__':
    user_degree_sequence = get_user_sequence()
    print("\nStarting Havel-Hakimi Algorithm for sequence:", user_degree_sequence)

    is_graphical, graph = realize_and_draw(user_degree_sequence, show=True)

    if is_graphical:
        print(f"Success! Constructed graph has {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.")
    else:
        print("Failed! The provided sequence is not graphical.")