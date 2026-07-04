import streamlit as st
import os
import matplotlib.pyplot as plt
import importlib.util
import sys
import io
import contextlib

st.set_page_config(page_title="Graph Theory & Combinatorics Lab", layout="wide")

st.markdown(
"""
<style>
header[data-testid="stHeader"], .stAppHeader {
    display: none !important;
}

.custom-header {
    background-color: #8bffa8; 
    height: 70px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 999999;
    padding: 0 20px;
    border-bottom: 2px solid #BBDEFB;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
}

.header-title {
    color: #000000; 
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    flex-grow: 1;
}

.header-img-left {
    height: 50px;
    width: 50px;
    object-fit: contain;
}

.header-spacer {
    width: 50px;
}

.st-key-fixed_nav {
    position: fixed;
    top: 70px;
    left: 0;
    right: 0;
    background-color: #5cff67;
    z-index: 999998;
    padding: 10px 40px;
    border-bottom: 1px solid #3d3e47;
}

.appview-container .main .block-container {
    padding-top: 10rem !important;
    padding-bottom: 5rem !important;
}
</style>

<div class="custom-header">
    <img src="app/static/GCElogo.png" class="header-img-left" alt="GCE Logo">
    <div class="header-title">Graph Theory & Combinatorics Lab</div>
    <div class="header-spacer"></div>
</div>
""",
    unsafe_allow_html=True
)

# st.subheader("Roll No: 24B-CO-016 | Semester 4 | Batch A | NEP RC-2024-25")

st.write("---")

if 'selected_exp_num' not in st.session_state:
    st.session_state.selected_exp_num = 1

with st.container(key="fixed_nav"):
    nav_cols = st.columns([1.5] + [1] * 11)

    with nav_cols[0]:
        st.markdown(
            "<div style='font-weight: bold; font-size: 16px; color: #ffffff; padding-top: 8px; text-align: center; background-color: #262730; border-radius: 5px; height: 38px;'>Experiment</div>", 
            unsafe_allow_html=True
        )

    for i in range(1, 12):
        button_style = "primary" if st.session_state.selected_exp_num == i else "secondary"
        if nav_cols[i].button(f"{i}", key=f"nav_btn_{i}", type=button_style, use_container_width=True):
            st.session_state.selected_exp_num = i
            st.rerun()

experiment = f"Experiment {st.session_state.selected_exp_num}"

experiment_data = {
    "Experiment 1": {
        "full_name": "Experiment 1: 29 / 01 / 2026",
        "aim": "To implement basic Graphs such as Complete graph, Path graph, Cycle graph, and Complete Bipartite graph.",
        "theory": "A mathematical abstraction of situations involving sets of points together with lines joining certain pairs of these points gives rise to the concept of a graph. Formally, a graph G is defined as an ordered triple (V(G), E(G), $\\psi_G$). This structure consists of a nonempty set V(G) of elements called vertices, a set E(G), strictly disjoint from V(G), of elements called edges, and an incidence function $\\psi_G$ that associates with each edge of G an unordered pair of (not necessarily distinct) vertices of G."
    },
    "Experiment 2": {
        "full_name": "Experiment 2: 05 / 02 / 2026",
        "aim": "To implement graph isomorphism verification in order to compare structural equivalence between two graphs.",
        "theory": "In the study of graph theory, graphs that are not identical can possess essentially the same diagram and structure, differing solely in the labels assigned to their vertices and edges. Such graphs are formally classified as isomorphic, which indicates that they share the exact same structural properties. In general, two graphs G and H are said to be isomorphic, mathematically denoted as G ≅ H, if there exist bijections $\\theta$ : V(G) -> V(H) and $\\phi$ : E(G) -> E(H) such that the adjacency structures are preserved."
    },
    "Experiment 3": {
        "full_name": "Experiment 3: 12 / 02 / 2026",
        "aim": "To implement generation of various subgraphs such induced subgraphs, spanning subgraphs and edge deleted subgraphs.",
        "theory": "In the mathematical study of graph theory, it is frequently necessary to analyze smaller internal structures contained within a broader graph system. A graph H is formally defined as a subgraph of a graph G, mathematically written as H ⊆ G, if its vertex set V(H) is a subset of V(G) (V(H) ⊆ V(G)), its edge set E(H) is a subset of E(G) (E(H) ⊆ E(G)), and the incidence function $\\psi_H$ is strictly the restriction of the incidence function $\\psi_G$ to E(H)."
    },
    "Experiment 4": {
        "full_name": "Experiment 4: 19 / 02 / 2026",
        "aim": "To implement the construction of a graph for a given degree sequence in order to realize the graphical sequence using Havel Hakimi algorithm.",
        "theory": "In the mathematical study of graph theory, it is often necessary to analyze the structural properties of a graph by examining the degrees of its vertices. If a graph G has vertices $v_1, v_2, \\dots, v_n$, the sequence of these vertex degrees, denoted as $(d(v_1), d(v_2), \\dots, d(v_n))$, is formally defined as a degree sequence of G. A fundamental condition dictates that a sequence of non-negative integers can be the degree sequence of some general graph if and only if the sum of degrees is even."
    },
    "Experiment 5": {
        "full_name": "Experiment 5: 12 / 03 / 2026",
        "aim": "Convert the original graph into its line graph, where each edge of the original graph becomes a vertex in the new graph, and adjacency is defined by shared endpoints in the original graph.",
        "theory": "In graph theory, the line graph frequently referred to as an edge graph, adjoint graph, or covering graph of an undirected graph G is a derivative graph L(G) that captures the adjacencies between the edges of G. It essentially translates the structural relationships of edges in the original graph into the vertex relationships of a completely new graph. The fundamental methodology for converting an original graph into its line graph relies on a direct, one-to-one mapping: each edge of the original graph becomes a distinct, independent vertex in the new line graph."
    },
    "Experiment 6": {
        "full_name": "Experiment 6: 02 / 04 / 2026",
        "aim": "To implement finding the minimum spanning tree for a given graph using Kruskal's algorithm, ensuring all vertices are connected with the minimum possible total edge weight and without forming cycles.",
        "theory": "In the mathematical study of graph theory and network optimization, it is frequently necessary to analyze the properties of weighted graphs. With each edge e of a graph G, let there be associated a real number w(e), called its weight, which makes G a weighted graph. If H is a subgraph of a weighted graph G, the total weight w(H) of H is defined mathematically as the sum of the weights on its edges, formally written as $w(H) = \\sum_{e \\in E(H)} w(e)$."
    },
    "Experiment 7": {
        "full_name": "Experiment 7: 09 / 04 / 2026 SP",
        "aim": "To implement shortest path algorithm in order to compute the shortest path from the source vertex to all the other vertices in a weighted graph.",
        "theory": "In the mathematical study of graph theory and network optimization, situations arise where distinct edges hold varying levels of significance or cost. With each edge e of a graph G, let there be associated a real number w(e), called its weight. The graph G, together with these explicitly defined weights on its edges, is formally classified as a weighted graph. If H is a subgraph of a weighted graph G, the total weight w(H) of H is defined mathematically as the sum of the weights on its constituent edges."
    },
    "Experiment 8": {
        "full_name": "Experiment 8: 30 / 04 / 2026",
        "aim": "To implement generation of closed walks, trail and path in a connected graph.",
        "theory": "In the mathematical study of graph theory and network optimization, the traversal of a graph is formalized through specific sequences of elements. A walk W in a graph G is mathematically defined as a finite non-null sequence $W = v_0 e_1 v_1 \\dots e_k v_k$, whose terms are alternately vertices and edges, such that for $1 \\le i \\le k$, the ends of edge $e_i$ are $v_{i-1}$ and $v_i$. The vertices $v_0$ and $v_k$ are designated as the origin and terminus of W, respectively."
    },
    "Experiment 9": {
        "full_name": "Experiment 9: 30 / 04 / 2026",
        "aim": "To implement an algorithm that checks for the existence of an Eulerian circuit, and construct the circuit that traverses every edge of the graph exactly once.",
        "theory": "In the mathematical study of graph theory, the traversal of a network is formalized through specific sequences of elements. A walk W in a graph G is defined mathematically as a finite non-null sequence $W = v_0 e_1 v_1 \\dots e_k v_k$, whose terms are alternately vertices and edges, such that the ends of each edge $e_i$ are $v_{i-1}$ and $v_i$. If the edges of a walk W are entirely distinct, the sequence is formally called a trail.  A walk is defined as closed if it possesses a positive length and its origin and terminus are  exactly the same vertex $(v_0 = v_k)$. An Euler tour, or Euler circuit, is explicitly defined as a closed trail that traverses every single edge of the graph exactly once. A graph is formally classified as eulerian if it contains an Euler circuit. "
    },
    "Experiment 10": {
        "full_name": "Experiment 10: 07 / 05 / 2026",
        "aim": "To implement a method to determine whether a graph contains a Hamiltonian circuit, that is a cycle that visits every vertex exactly once.",
        "theory": "In the mathematical study of graph theory, the traversal of a graph is formalized through specific sequences of elements. A walk W in a graph G is mathematically defined as a finite non-null sequence $W = v_0 e_1 v_1 \\dots e_k v_k$, whose terms are alternately vertices and edges, such that for $1 \\le i \\le k$, the ends of edge $e_i$ are $v_{i-1}$ and $v_i$. The topological distinction between open and closed substructures relies on the mathematical equivalence of the starting and ending points."
    },
    "Experiment 11": {
        "full_name": "Experiment 11: 14 / 05 / 2026",
        "aim": "To implement the Greedy graph coloring algorithm that assigns colors to the vertices such that no two adjacent vertices share the same color with minimum chromatic number.",
        "theory": "In the mathematical study of graph theory, vertex coloring constitutes a fundamental partition problem with broad theoretical implications. Formally, a k-vertex coloring of a loopless graph G is an assignment of k colors, typically represented by the integers $1,2,\\dots,k$, to the vertices of G. This coloring is strictly defined as proper if no two distinct adjacent vertices share the same color."
    }
}

st.header(experiment_data[experiment]["full_name"])

st.subheader("Aim of Experiment")
st.write(experiment_data[experiment]["aim"])

st.subheader("Theory")
st.write(experiment_data[experiment]["theory"])

st.write("---")

def read_code_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return f"# File not found at: {filepath}"

def run_experiment_file(filepath):
    plt.clf()
    plt.close('all')
    
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                exec(file.read(), globals())
            fig = plt.gcf()
            return fig
        except Exception as e:
            st.error(f"Error running script: {e}")
            return None
    return None

def run_experiment_with_console(filepath, input_list=None):
    plt.clf()
    plt.close('all')
    
    captured_output = ""
    fig = None
    
    if os.path.exists(filepath):
        try:
            f = io.StringIO()
            custom_globals = dict(globals())
            
            if input_list is not None:
                input_iter = iter(input_list)
                def mock_input(prompt=""):
                    try:
                        val = next(input_iter)
                        print(f"{prompt}{val}") 
                        return val
                    except StopIteration:
                        return ""
                custom_globals['input'] = mock_input
            
            with contextlib.redirect_stdout(f):
                with open(filepath, "r", encoding="utf-8") as file:
                    exec(file.read(), custom_globals)
            
            captured_output = f.getvalue()
            fig = plt.gcf()
            
            return fig, captured_output
        except Exception as e:
            st.error(f"Error running script: {e}")
            return None, f"Error executing script logic: {e}"
            
    return None, "File not found."

if experiment == "Experiment 1":
    approach = st.radio(
        "Choose Implementation Type:",
        ["Dedicated Built-in NetworkX Functions", "No dedicated NetworkX Built-in Function"]
    )
    
    st.write("---")
    folder_path = "01 - 29 January"
    
    if approach == "Dedicated Built-in NetworkX Functions":
        st.subheader("Approach: Using NetworkX Dedicated Functions")
        
        file_path = os.path.join(folder_path, "final_graphs.py")        
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")

        st.subheader("Output: ")
        if st.button(">>  Run Code", key="run_nx", type="primary"):
            with st.spinner("Executing script and generating graph..."):
                fig_output = run_experiment_file(file_path)
                if fig_output:
                    st.pyplot(fig_output)
        
        st.subheader("Conclusion")
        st.info("Basic Graphs such as Complete graph, Cycle graph, Path graph and Complete Bipartite graph were implemented successfully.")

    elif approach == "No dedicated NetworkX Built-in Function":
        st.subheader("Approach: Flowchart/Manual/Algorithm Implementation")
        
        file_path = os.path.join(folder_path, "final_graphs_not_nx.py")        
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")

        st.subheader("Output: ")
        if st.button(">>  Run Code", key="run_no_nx", type="primary"):
            with st.spinner("Executing script and generating graph..."):
                fig_output = run_experiment_file(file_path)
                if fig_output:
                    st.pyplot(fig_output)
        
        st.subheader("Conclusion")
        st.info("Basic Graphs such as Complete graph, Cycle graph, Path graph and Complete Bipartite graph were implemented successfully.")

elif experiment == "Experiment 2":
    approach = st.radio(
        "Choose Implementation Type:",
        ["Dedicated Built-in NetworkX Functions", "No dedicated NetworkX Built-in Function"]
    )

    st.write("---")
    folder_path = "02 - 05 February"
    
    if approach == "Dedicated Built-in NetworkX Functions":
        st.subheader("Approach: Using NetworkX Dedicated Functions")
        
        file_path = os.path.join(folder_path, "expt_02_inbuilt.py")
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")

        st.subheader("Output: ")
        if st.button(">>  Run Code", key="run_nx", type="primary"):
            with st.spinner("Executing script and generating graph..."):
                fig_output = run_experiment_file(file_path)
                if fig_output:
                    st.pyplot(fig_output)
        
        st.subheader("Conclusion")
        st.info("Graph isomorphism verification in order to compare structural equivalence between two graphs was implemented successfully.")

    elif approach == "No dedicated NetworkX Built-in Function":
        st.subheader("Approach: Flowchart/Manual/Algorithm Implementation")
                
        file_path = os.path.join(folder_path, "expt_02_no_inbuilt.py")
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")

        st.subheader("Output: ")
        if st.button(">>  Run Code", key="run_no_nx", type="primary"):
            with st.spinner("Executing script and generating graph..."):
                fig_output = run_experiment_file(file_path)
                if fig_output:
                    st.pyplot(fig_output)
        
        st.subheader("Conclusion")
        st.info("Graph isomorphism verification in order to compare structural equivalence between two graphs was implemented successfully.")

elif experiment == "Experiment 3":
    approach = st.radio(
        "Choose Implementation Type:",
        ["Dedicated Built-in NetworkX Functions", "No dedicated NetworkX Built-in Function"]
    )

    st.write("---")
    folder_path = "03 - 12 February"
    
    if approach == "Dedicated Built-in NetworkX Functions":
        st.subheader("Approach: Using NetworkX Dedicated Functions")
        
        file_path = os.path.join(folder_path, "expt_03_inbuilt.py")
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")
        
        st.subheader("Output: ")
        if st.button(">>  Run Code", key="run_nx", type="primary"):
            with st.spinner("Executing script and generating graph..."):
                fig_output, console_text = run_experiment_with_console(file_path, input_list=None)
                if fig_output:
                    st.pyplot(fig_output)

                if console_text.strip():
                    st.subheader("Console Output")
                    st.code(console_text, language="text")
        
        st.subheader("Conclusion")
        st.info("Generation of various subgraphs such induced subgraphs, spanning subgraphs and edge deleted subgraphs was implemented successfully. ")

    elif approach == "No dedicated NetworkX Built-in Function":
        st.subheader("Approach: Flowchart/Manual/Algorithm Implementation")
        file_path = os.path.join(folder_path, "expt_03_subgr_inbuilt.py")
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")

        st.markdown("### Enter Input")
        st.info("Adjust parameters to view the type of Subgraph: ")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Vertex Induced Subgraph Constraints**")
            n_vertices = st.number_input(
                "How many vertices do you want to keep?", 
                min_value=1, max_value=50, value=3, step=1
            )
            vertices_str = st.text_input(
                "Enter individual vertex numbers (comma-separated):", 
                value="0, 1, 2"
            )
            
        with col2:
            st.markdown("**Edge Deletion Constraints**")
            edge_v1 = st.text_input("Enter the first vertex of edge to delete:", value="0")
            edge_v2 = st.text_input("Enter the second vertex of edge to delete:", value="1")
        
        st.write("---")
        
        parsed_vertices = [v.strip() for v in vertices_str.split(",") if v.strip()]
        
        runtime_inputs = [str(n_vertices)] + parsed_vertices + [str(edge_v1), str(edge_v2)]
        
        st.subheader("Output: ")
        if st.button(">>  Run Code", key="run_no_nx", type="primary"):
            with st.spinner("Processing configurations and rendering graph matrices..."):
                fig_output, console_text = run_experiment_with_console(file_path, input_list=runtime_inputs)
                
                if fig_output:
                    st.pyplot(fig_output)

                if console_text.strip():
                    st.subheader("Console Log")
                    st.code(console_text, language="text")
        
        st.subheader("Conclusion")
        st.info("Generation of various subgraphs such induced subgraphs, spanning subgraphs and edge deleted subgraphs was implemented successfully. ")

elif experiment == "Experiment 4":
    approach = st.radio(
        "Choose Implementation Type:",
        ["Dedicated Built-in NetworkX Functions", "No dedicated NetworkX Built-in Function"]
    )

    st.write("---")
    folder_path = "04 - 19 February"
    
    if approach == "Dedicated Built-in NetworkX Functions":
        st.subheader("Approach: Using NetworkX Dedicated Functions")
                
        file_path = os.path.join(folder_path, "expt_04_inbuilt_nx.py")
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")
        
        st.markdown("### User Input Section")
        st.info("Provide the degree sequence below to check graphical validity or plot the network logic.")

        degree_seq = st.text_input(
            "Enter a degree sequence separated by spaces:", 
            value="7 6 6 5 4 4 3 2 1 1"
        )

        st.write("---")
        runtime_inputs = [degree_seq.strip()]

        st.subheader("Output: ")
        if st.button(">>  Run Code", key="run_nx", type="primary"):
            with st.spinner("Processing degree sequence and rendering graph..."):
                fig_output, console_text = run_experiment_with_console(file_path, input_list=runtime_inputs)            

                if console_text.strip():
                    st.subheader("Console Log")
                    st.code(console_text, language="text")        
        
        st.subheader("Conclusion")
        st.info("The construction of a graph for a given degree sequence in order to realize the graphical sequence using Havel Hakimi algorithm was implemented successfully.")

    elif approach == "No dedicated NetworkX Built-in Function":
        st.subheader("Approach: Flowchart/Manual/Algorithm Implementation")
        
        file_path = os.path.join(folder_path, "expt_04_without_inbuilt.py")
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")

        st.markdown("### User Input Section")
        st.info("Provide the degree sequence below to check graphical validity or plot the network logic.")
        
        degree_seq = st.text_input(
            "Enter a degree sequence separated by spaces:", 
            value="7 6 6 5 4 4 3 2 1 1"
        )
        
        st.write("---")
        
        runtime_inputs = [degree_seq.strip()]
        
        st.subheader("Output: ")
        if st.button(">>  Run Code", key="run_no_nx", type="primary"):
            with st.spinner("Processing degree sequence and rendering graph..."):
                fig_output, console_text = run_experiment_with_console(file_path, input_list=runtime_inputs)
                
                if fig_output:
                    st.pyplot(fig_output)

                if console_text.strip():
                    st.subheader("Console Log")
                    st.code(console_text, language="text")        
        
        st.subheader("Conclusion")
        st.info("The construction of a graph for a given degree sequence in order to realize the graphical sequence using Havel Hakimi algorithm was implemented successfully.")

elif experiment == "Experiment 5":
    approach = st.radio(
        "Choose Implementation Type:",
        ["Dedicated Built-in NetworkX Functions", "No dedicated NetworkX Built-in Function"]
    )

    st.write("---")
    folder_path = "05 - 12 March"
    
    if approach == "Dedicated Built-in NetworkX Functions":
        st.subheader("Approach: Using NetworkX Dedicated Functions")
        file_path = os.path.join(folder_path, "expt_05_inbuilt_func.py")
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")

        st.markdown("### User Input Section")
        st.info("Enter the number of vertices, then fill out the adjacency matrix row by row.")

        n_vertices = st.number_input(
            "Enter the number of vertices in the original graph:", 
            min_value=1, max_value=20, value=4, step=1
        )

        st.markdown("**Enter the adjacency matrix row by row (space-separated values):**")

        default_matrix = ["0 1 1 1", "1 0 0 0", "1 0 0 0", "1 0 0 0"]
        
        matrix_inputs = []
        
        for i in range(int(n_vertices)):
            if n_vertices == 4 and i < len(default_matrix):
                default_val = default_matrix[i]
            else:
                row_template = ["0"] * int(n_vertices)
                if i < int(n_vertices) - 1:
                    row_template[i + 1] = "1"
                if i > 0:
                    row_template[i - 1] = "1"
                default_val = " ".join(row_template)
            
            row_input = st.text_input(
                f"Row {i + 1}:", 
                value=default_val, 
                key=f"exp5_inbuilt_row_{i}"
            )
            matrix_inputs.append(row_input.strip())

        st.write("---")
        
        runtime_inputs = [str(n_vertices)] + matrix_inputs

        st.subheader("Output: ")
        if st.button(">>  Run Code", key="run_nx", type="primary"):
            with st.spinner("Processing adjacency matrix and rendering graph..."):
                fig_output, console_text = run_experiment_with_console(file_path, input_list=runtime_inputs)
                
                if fig_output:
                    st.pyplot(fig_output)

                if console_text.strip():
                    st.subheader("Console Log")
                    st.code(console_text, language="text")        
        
        st.subheader("Conclusion")
        st.info("Conversion of the given original graph into its line graph, where each edge of the original graph becomes a vertex in the new graph, and adjacency is defined by shared endpoints in the original graph was implemented successfully. ")

    elif approach == "No dedicated NetworkX Built-in Function":
        st.subheader("Approach: Flowchart/Manual/Algorithm Implementation")
        
        file_path = os.path.join(folder_path, "expt_05_no_inbuilt.py")
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")
        
        st.markdown("### User Input Section")
        st.info("Enter the number of vertices, then fill out the adjacency matrix row by row.")
        
        n_vertices = st.number_input(
            "Enter the number of vertices in the original graph:", 
            min_value=1, max_value=20, value=4, step=1
        )        
        st.markdown("**Enter the adjacency matrix row by row (space-separated values):**")
        default_matrix = ["0 1 1 1", "1 0 0 0", "1 0 0 0", "1 0 0 0"]
        matrix_inputs = []
        for i in range(int(n_vertices)):
            if n_vertices == 4 and i < len(default_matrix):
                default_val = default_matrix[i]
            else:
                row_template = ["0"] * int(n_vertices)
                if i < int(n_vertices) - 1:
                    row_template[i + 1] = "1"
                if i > 0:
                    row_template[i - 1] = "1"
                default_val = " ".join(row_template)
            
            row_input = st.text_input(
                f"Row {i + 1}:", 
                value=default_val, 
                key=f"exp5_no_inbuilt_row_{i}"
            )
            matrix_inputs.append(row_input.strip())

        st.write("---")
        runtime_inputs = [str(n_vertices)] + matrix_inputs
        st.subheader("Output: ")
        if st.button(">>  Run Code", key="run_no_nx", type="primary"):
            with st.spinner("Processing adjacency matrix and rendering graph..."):
                fig_output, console_text = run_experiment_with_console(file_path, input_list=runtime_inputs)
                
                if fig_output:
                    st.pyplot(fig_output)

                if console_text.strip():
                    st.subheader("Console Log")
                    st.code(console_text, language="text")        
        
        st.subheader("Conclusion")
        st.info("Conversion of the given original graph into its line graph, where each edge of the original graph becomes a vertex in the new graph, and adjacency is defined by shared endpoints in the original graph was implemented successfully. ")

elif experiment == "Experiment 6":
    approach = st.radio(
        "Choose Implementation Type:",
        ["Dedicated Built-in NetworkX Functions", "No dedicated NetworkX Built-in Function"]
    )

    st.write("---")
    folder_path = "06 - 02 April"
    
    if approach == "Dedicated Built-in NetworkX Functions":
        st.subheader("Approach: Using NetworkX Dedicated Functions")
                
        file_path = os.path.join(folder_path, "expt06_inbuilt.py")
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")
        
        st.subheader("Output: ")
        if st.button(">>  Run Code", key="run_nx", type="primary"):
            with st.spinner("Executing script and generating graph..."):
                fig_output = run_experiment_file(file_path)
                if fig_output:
                    st.pyplot(fig_output)        
        
        st.subheader("Conclusion")
        st.info("Finding the minimum spanning tree for a given graph using Kruskal's algorithm, ensuring all vertices are connected with the minimum possible total edge weight and without forming cycles was implemented successfully. ")

    elif approach == "No dedicated NetworkX Built-in Function":
        st.subheader("Approach: Flowchart/Manual/Algorithm Implementation")
                
        file_path = os.path.join(folder_path, "expt_06_flowchart_n.py")
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")
        
        st.subheader("Output: ")
        if st.button(">>  Run Code", key="run_no_nx", type="primary"):
            with st.spinner("Generating graph..."):
                fig_output = run_experiment_file(file_path)
                if fig_output:
                    st.pyplot(fig_output)                    
        
        st.subheader("Conclusion")
        st.info("Finding the minimum spanning tree for a given graph using Kruskal's algorithm, ensuring all vertices are connected with the minimum possible total edge weight and without forming cycles was implemented successfully. ")

elif experiment == "Experiment 7":
    approach = st.radio(
        "Choose Implementation Type:",
        ["Dedicated Built-in NetworkX Functions", "No dedicated NetworkX Built-in Function"]
    )

    st.write("---")
    folder_path = "07 - 09 April SP"
    
    if approach == "Dedicated Built-in NetworkX Functions":
        st.subheader("Approach: Using NetworkX Dedicated Functions")
                
        file_path = os.path.join(folder_path, "shortest_path_inbuilt.py")
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")
        
        st.subheader("Output: ")
        if st.button(">>  Run Code", key="run_nx", type="primary"):
            with st.spinner("Executing script and generating graph..."):
                fig_output, console_text = run_experiment_with_console(file_path, input_list=None)
                if fig_output:
                    st.pyplot(fig_output)

                if console_text.strip():
                    st.subheader("Console Log")
                    st.code(console_text, language="text")        
        
        st.subheader("Conclusion")
        st.info("Shortest path algorithm in order to compute the shortest path from the source vertex to all the other vertices in a weighted graph was implemented successfully. ")

    elif approach == "No dedicated NetworkX Built-in Function":
        st.subheader("Approach: Flowchart/Manual/Algorithm Implementation")
                
        file_path = os.path.join(folder_path, "shortest_path_non_inbuilt.py")
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")
        
        st.subheader("Output: ")
        if st.button(">>  Run Code", key="run_no_nx", type="primary"):
            with st.spinner("Generating graph..."):
                fig_output, console_text = run_experiment_with_console(file_path, input_list=None)
                if fig_output:
                    st.pyplot(fig_output)

                if console_text.strip():
                    st.subheader("Console Log")
                    st.code(console_text, language="text")        
        
        st.subheader("Conclusion")
        st.info("Shortest path algorithm in order to compute the shortest path from the source vertex to all the other vertices in a weighted graph was implemented successfully. ")

elif experiment == "Experiment 8":
    approach = st.radio(
        "Choose Implementation Type:",
        ["Dedicated Built-in NetworkX Functions", "No dedicated NetworkX Built-in Function"]
    )

    st.write("---")
    folder_path = "08 - 30 April"
    
    if approach == "Dedicated Built-in NetworkX Functions":
        st.subheader("Approach: Using NetworkX Dedicated Functions")
        
        st.subheader("Output: ")
        file_path = os.path.join(folder_path, "exp_08_inbuilt.py")
        
        if st.button(">>  Run Code", key="run_nx", type="primary"):
            with st.spinner("Executing script and rendering both canvases..."):
                plt.clf()
                plt.close('all')
                
                if os.path.exists(file_path):
                    try:
                        exp8_context = dict(globals())
                        
                        with open(file_path, "r", encoding="utf-8") as file:
                            exec(file.read(), exp8_context)
                        
                        tab1, tab2 = st.tabs(["Canvas 1: Graph 1 Analysis", "Canvas 2: Graph 2 Analysis"])
                        
                        with tab1:
                            if 'fig1' in exp8_context:
                                st.pyplot(exp8_context['fig1'])
                            else:
                                st.warning("Figure 'fig1' was not found in the script execution context.")
                                
                        with tab2:
                            if 'fig2' in exp8_context:
                                st.pyplot(exp8_context['fig2'])
                            else:
                                st.warning("Figure 'fig2' was not found in the script execution context.")
                                
                    except Exception as e:
                        st.error(f"Error running Experiment 8 script: {e}")
                else:
                    st.error(f"File not found at: {file_path}")
        
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")
        
        st.subheader("Conclusion")
        st.info("Generation of closed walks, trail and path in a connected graph was implemented successfully. ")

    elif approach == "No dedicated NetworkX Built-in Function":
        st.subheader("Approach: Flowchart/Manual/Algorithm Implementation")
        
        folder_path = "08 - 30 April" 
        file_path = os.path.join(folder_path, "exp_08_no_inbuilt.py")
        
        st.subheader("Output: ")
        
        if st.button(">>  Run Code", key="run_no_nx", type="primary"):
            with st.spinner("Executing script and rendering both canvases..."):
                plt.clf()
                plt.close('all')
                
                if os.path.exists(file_path):
                    try:
                        exp8_context = dict(globals())
                        
                        with open(file_path, "r", encoding="utf-8") as file:
                            exec(file.read(), exp8_context)
                        
                        tab1, tab2 = st.tabs(["Canvas 1: Graph 1 Analysis", "Canvas 2: Graph 2 Analysis"])
                        
                        with tab1:
                            if 'fig1' in exp8_context:
                                st.pyplot(exp8_context['fig1'])
                            else:
                                st.warning("Figure 'fig1' was not found in the script execution context.")
                                
                        with tab2:
                            if 'fig2' in exp8_context:
                                st.pyplot(exp8_context['fig2'])
                            else:
                                st.warning("Figure 'fig2' was not found in the script execution context.")
                                
                    except Exception as e:
                        st.error(f"Error running Experiment 8 script: {e}")
                else:
                    st.error(f"File not found at: {file_path}")
                
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")
        
        st.subheader("Conclusion")
        st.info("Generation of closed walks, trail and path in a connected graph was implemented successfully. ")

elif experiment == "Experiment 9":
    approach = st.radio(
        "Choose Implementation Type:",
        ["Dedicated Built-in NetworkX Functions", "No dedicated NetworkX Built-in Function"]
    )

    st.write("---")
    folder_path = "09 - 30 April"
    
    if approach == "Dedicated Built-in NetworkX Functions":
        st.subheader("Approach: Using NetworkX Dedicated Functions")
        
        st.subheader("Output: ")
        file_path = os.path.join(folder_path, "exp09_inbuilt.py")
        
        if st.button(">>  Run Code", key="run_nx", type="primary"):
            with st.spinner("Executing script and generating graph..."):
                fig_output = run_experiment_file(file_path)
                if fig_output:
                    st.pyplot(fig_output)
        
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")
        
        st.subheader("Conclusion")
        st.info("An algorithm that checks for the existence of an Eulerian circuit, and then construct the circuit that traverses every edge of the graph exactly once was implemented successfully. ")

    elif approach == "No dedicated NetworkX Built-in Function":
        st.subheader("Approach: Flowchart/Manual/Algorithm Implementation")
        
        folder_path = "09 - 30 April" 
        file_path = os.path.join(folder_path, "exp09_no_inbuilt.py")
        
        st.subheader("Output: ")
        
        if st.button(">>  Run Code", key="run_no_nx", type="primary"):
            with st.spinner("Executing script and rendering both canvases..."):
                plt.clf()
                plt.close('all')
                
                if os.path.exists(file_path):
                    try:
                        exp9_context = dict(globals())
                        
                        with open(file_path, "r", encoding="utf-8") as file:
                            exec(file.read(), exp9_context)
                        
                        tab1, tab2 = st.tabs(["Canvas 1: Graph 1 Analysis", "Canvas 2: Graph 2 Analysis"])
                        
                        with tab1:
                            if 'fig1' in exp9_context:
                                st.pyplot(exp9_context['fig1'])
                            else:
                                st.warning("Figure 'fig1' was not found in the script execution context.")
                                
                        with tab2:
                            if 'fig2' in exp9_context:
                                st.pyplot(exp9_context['fig2'])
                            else:
                                st.warning("Figure 'fig2' was not found in the script execution context.")
                                
                    except Exception as e:
                        st.error(f"Error running Experiment 9 script: {e}")
                else:
                    st.error(f"File not found at: {file_path}")
                
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")
        
        st.subheader("Conclusion")
        st.info("An algorithm that checks for the existence of an Eulerian circuit, and then construct the circuit that traverses every edge of the graph exactly once was implemented successfully. ")

elif experiment == "Experiment 10":
    approach = st.radio(
        "Choose Implementation Type:",
        ["Manual"]
    )

    st.write("---")
    folder_path = "10 - 07 May"
    
    if approach == "Manual":
        st.subheader("Approach: Manual")
        
        st.subheader("Output: ")
        file_path = os.path.join(folder_path, "exp_10_inbuilt.py")
        
        if st.button(">>  Run Code", key="run_nx", type="primary"):
            with st.spinner("Executing script and rendering both canvases..."):
                plt.clf()
                plt.close('all')
                
                if os.path.exists(file_path):
                    try:
                        exp10_context = dict(globals())
                        
                        with open(file_path, "r", encoding="utf-8") as file:
                            exec(file.read(), exp10_context)
                        
                        tab1, tab2 = st.tabs(["Canvas 1: Graph 1 Analysis", "Canvas 2: Graph 2 Analysis"])
                        
                        with tab1:
                            if 'fig1' in exp10_context:
                                st.pyplot(exp10_context['fig1'])
                            else:
                                st.warning("Figure 'fig1' was not found in the script execution context.")
                                
                        with tab2:
                            if 'fig2' in exp10_context:
                                st.pyplot(exp10_context['fig2'])
                            else:
                                st.warning("Figure 'fig2' was not found in the script execution context.")
                                
                    except Exception as e:
                        st.error(f"Error running Experiment 10 script: {e}")
                else:
                    st.error(f"File not found at: {file_path}")
        
        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")
        
        st.subheader("Conclusion")
        st.info("Python program method to determine whether a graph contains a Hamiltonian circuit, that is a cycle that visits every vertex exactly once was implemented successfully. ")

elif experiment == "Experiment 11":
    approach = st.radio(
        "Choose Implementation Type:",
        ["Dedicated Built-in NetworkX Functions", "No dedicated NetworkX Built-in Function", "Sudoku Problem"]
    )

    st.write("---")
    folder_path = "11 - 14 May"
    
    if approach == "Dedicated Built-in NetworkX Functions":
        st.subheader("Approach: Using NetworkX Dedicated Functions")
        
        st.subheader("Output: ")
        file_path = os.path.join(folder_path, "expt11_inbuilt.py")

        if st.button(">>  Run Code", key="run_nx", type="primary"):        
            with st.spinner("Executing script and generating graph..."):
                fig_output = run_experiment_file(file_path)
                if fig_output:
                    st.pyplot(fig_output)

        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")
        
        st.subheader("Conclusion")
        st.info("Greedy graph coloring algorithm that assigns colors to the vertices such that no two adjacent vertices share the same color with minimum chromatic number was implemented successfully.  ")

    elif approach == "No dedicated NetworkX Built-in Function":
        st.subheader("Approach: Flowchart/Manual/Algorithm Implementation")
        
        st.subheader("Output: ")
        file_path = os.path.join(folder_path, "expt11_no_inbuilt.py")
        
        if st.button(">>  Run Code", key="run_nx", type="primary"):
            with st.spinner("Generating graph..."):
                fig_output = run_experiment_file(file_path)
                if fig_output:
                    st.pyplot(fig_output)

        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")
        
        st.subheader("Conclusion")
        st.info("Greedy graph coloring algorithm that assigns colors to the vertices such that no two adjacent vertices share the same color with minimum chromatic number was implemented successfully.  ")

    elif approach == "Sudoku Problem":
        st.subheader("Approach: Sudoku Problem")
        
        st.subheader("Output: ")
        file_path = os.path.join(folder_path, "expt11_sud.py")
        
        if st.button(">>  Run Code", key="run_nx", type="primary"):
            with st.spinner("Executing script and generating graph..."):
                fig_output = run_experiment_file(file_path)
                if fig_output:
                    st.pyplot(fig_output)

        code_content = read_code_file(file_path)
        with st.expander("View Python Source Code", expanded=False):
            st.code(code_content, language="python")
        
        st.subheader("Conclusion")
        st.info("Greedy graph coloring algorithm that assigns colors to the vertices such that no two adjacent vertices share the same color with minimum chromatic number was implemented successfully.  ")

st.write("---")
st.markdown(
    """
    <style>
    .stApp {
        overflow-x: hidden;
    }

    .custom-footer {
        background-color: #8bffa8;
        color: #000000;
        text-align: center;
        padding: 10px 0;
        width: 100vw;
        
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;

        z-index: 999999; 
        border-top: 2px solid #6cd989;
        font-weight: 500;
    }

    .appview-container .main .block-container {
        padding-bottom: 6rem !important; 
    }
    </style>
    <div class="custom-footer">
        Name: Daksh Deepak Naik | Roll No: 24B-CO-016 | Semester 4 Batch A
    </div>
    """,
    unsafe_allow_html=True
)