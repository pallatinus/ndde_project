import pandas as pd
import networkx as nx
from src.models.novel_trevisan_de import NovelTrevisanDE
from src.trevisan.algorithms import *
from src.utils.graph import create_graph
from src.utils.files import list_files
import time


df = pd.DataFrame()
run_time = []
cuts = []
best_R = []
best_L = []
best_V = []
gens = []
graph_name = []
num_edges = []
num_vertices = []
depth = []


def main_iterative_evolutionary(graph):
    adj_matrix = nx.adjacency_matrix(graph).toarray()
    adj_list = get_adj_list(adj_matrix)
    active_vertices = [i for i in range(len(adj_matrix))]

    n = len(adj_matrix)
    x = find_smalles_eigenvector(adj_matrix, n)

    num_gen = 50
    mut_par = 1.2
    pop_size = 10

    problem_size = 40
    problem_partition_size = 10

    de = NovelTrevisanDE(vertices_num=n,
                         active_verts=active_vertices,
                         adj_matrix=adj_matrix,
                         adj_list=adj_list,
                         min_aigenvector=x,
                         population_size=pop_size,
                         problem_size=problem_size,
                         problem_batch_size=problem_partition_size,
                         mutation_parameter=mut_par,
                         number_generations=num_gen)

    R, L, V, cut_val, k, lsg, num_gen, mut_par, pop_size, pop_fit_history = de.evolutionary_process()
    return R, L, V, cut_val, k, lsg, num_gen, mut_par, pop_size, pop_fit_history


def main_evolutionary(graph):

    adj_matrix = nx.adjacency_matrix(graph).toarray()
    adj_list = get_adj_list(adj_matrix)
    active_vertices = [i for i in range(len(adj_matrix))]

    n = len(adj_matrix)
    x = find_smalles_eigenvector(adj_matrix, n)

    num_gen = 60
    mut_par = 0.50
    pop_size = 6

    de = NovelTrevisanDE(vertices_num=n,
                         active_verts=active_vertices,
                         adj_matrix=adj_matrix,
                         adj_list=adj_list,
                         min_aigenvector=x,
                         population_size = pop_size,
                         problem_size = 10,
                         mutation_parameter = mut_par,
                         number_generations = num_gen)

    y, cut_val, k, lsg, num_gen, mut_par, pop_size, pop_fit_history = de.evolutionary_process()
    return y, cut_val, k, lsg, num_gen, mut_par, pop_size, pop_fit_history


if __name__ == '__main__':
    path = "../data/max_cut"
    files = list_files(path)

    mutation_rates = []
    population_size = []


    for file in files:
        graph = create_graph(path, file)
        print(f"[Working with Graph: {file}]\n")

        start_cpu_time = time.process_time()
        R, L, V, cut_val, k, lsg, num_gen, mut_par, pop_size, pop_fit_history = main_iterative_evolutionary(graph)
        end_cpu_time = time.process_time()

        clock = end_cpu_time - start_cpu_time
        run_time.append(clock)
        print(f"\nTime = {clock}")

        cuts.append(cut_val)
        print(f"Number of Cuts = {cut_val}")

        best_R.append(R)
        print(f"Partition R = {R}")

        best_L.append(L)
        print(f"Partition L = {L}")

        best_V.append(V)
        print(f"Partition V = {V}")

        gens.append(k)
        print(f"Generations = {k}")

        depth.append(lsg)
        print(f"Depth = {lsg}")

        graph_name.append(file)
        print(f"graph = {file}")

        num_vertices.append(graph.number_of_nodes())
        print(f"Number of Vertices = {graph.number_of_nodes()}")

        num_edges.append(graph.number_of_edges())
        print(f"Number of Edges = {graph.number_of_edges()}\n")

    df['graph'] = graph_name
    df['cuts'] = cuts
    df['best_R'] = best_R
    df['best_L'] = best_L
    df['best_V'] = best_V
    df['generations'] = gens
    df['vertices'] = num_vertices
    df['edges'] = num_edges
    df['time'] = run_time
    df['depth'] = depth
    df['g_max'] = num_gen
    df['mutation'] = mut_par
    df['population'] = pop_size

    df.head()

    df.to_csv("../statistics/csv_files/data_iterative_evolutionary.csv")
