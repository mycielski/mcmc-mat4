import itertools
import random

import matplotlib.pyplot as plt
import networkx as nx


def check_if_valid_coloring(g, kcoloring):
    for pair in itertools.combinations(range(len(g)), 2):
        if (g[pair[0]][pair[1]] == 1) and (kcoloring[pair[0]] == kcoloring[pair[1]]):
            return False

    return True


def generate_random_graph(
    nodes, edge_probability=0.3, must_be_connected=False, must_be_planar=False
):
    g = nx.erdos_renyi_graph(nodes, edge_probability)
    if must_be_connected and not must_be_planar:
        while not nx.is_connected(g):
            g = nx.erdos_renyi_graph(nodes, edge_probability)
    elif not must_be_connected and must_be_planar:
        while not nx.algorithms.check_planarity(g, counterexample=False)[0]:
            g = nx.erdos_renyi_graph(nodes, edge_probability)
    elif must_be_connected and must_be_planar:
        while (
            not nx.is_connected(g)
            or not nx.algorithms.check_planarity(g, counterexample=False)[0]
        ):
            g = nx.erdos_renyi_graph(nodes, edge_probability)
    return g


def draw_graph(graph, title, coloring=None):
    if nx.algorithms.check_planarity(graph, counterexample=False)[0]:
        nx.draw_planar(graph, node_color=coloring, with_labels=True)
    else:
        nx.draw_spring(graph, node_color=coloring, with_labels=True)
    plt.title(title, x=0.5, y=0.95, fontsize=10)
    plt.show()


# this method returns a list of k different random colors
def random_colors(k):
    colors = set()
    while len(colors) < k:
        colors.add(random.randint(0, 255 ** 3))
    return list(colors)


# Zadanie 1
def z1(g):
    i = 1

    node_colors = [random.choice(colors) for _ in range(len(g))]

    while check_if_valid_coloring(g, node_colors) == False:
        node_colors = [random.choice(colors) for _ in range(len(g))]

    return node_colors


# Zadanie 2
def z2(g, x0):
    last_valid_coloring = x0

    node_colors = x0
    for n in range(30_000):
        node_colors[random.randint(0, len(node_colors) - 1)] = random.choice(colors)
        if check_if_valid_coloring(g, node_colors):
            last_valid_coloring = node_colors.copy()

    return last_valid_coloring


if __name__ == "__main__":
    n = int(input("Podaj liczbę wierzchołków grafu G: "))
    k = int(input("Podaj liczbę kolorów: "))

    if n < 1 or k < 1:
        raise ValueError("Liczby n i k muszą być dodatnie")

    # create graph with random edges
    graph = generate_random_graph(n)
    draw_graph(graph, "Graf G")

    # create adjacency matrix
    adj = nx.to_numpy_array(graph)

    # create k sized set of RGB colors
    colors = random_colors(k)

    print("\nZadanie 1")
    z1coloring = z1(adj)
    for index, color in enumerate(z1coloring):
        print("Wierzchołek", index, ":", hex(color), end="\n")
    draw_graph(graph, "Zadanie 1", z1coloring)

    print("\nZadanie 2")
    z2coloring = z2(adj, z1coloring)
    draw_graph(graph, "Zadanie 2", z2coloring)
    for index, color in enumerate(z2coloring):
        print("Wierzchołek", index, ":", hex(color), end="\n")

    z2colorings = list()
    for i in range(3000):
        z2colorings.append("".join([str(x) for x in z2(adj, z1coloring)]))

    plt.hist(z2colorings, bins=len(set(z2colorings)))
    plt.xticks("")
    plt.title("Histogram k-kolorowań")
    plt.show()
