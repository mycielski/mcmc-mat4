import itertools
import random
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from math import *


def check_if_valid_coloring(g, kcoloring):
    for pair in itertools.combinations(range(len(g)), 2):
        if (g[pair[0]][pair[1]] == 1) and (kcoloring[pair[0]] == kcoloring[pair[1]]):
            return False

    return True


def generate_random_graph(
    nodes, edge_probability=0.3, must_be_connected=True, must_be_planar=False
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


# Zadanie 3
lam = 6


def T(i, j):
    if i == 0:
        if j == 0 or j == 1:
            return 1 / 2
        return 0
    if j == i - 1 or j == i + 1:
        return 1 / 2
    else:
        return 0


def pi(i):
    return exp(-lam) * (lam ** i) / factorial(i)


def a_function(i, j):
    if T(i, j) == T(j, i):
        return pi(j) / pi(i)
    res = pi(j) * T(j, i) / (pi(j) * T(i, j))
    return res


def print_a(n):
    for i in range(0, n):
        for j in range(0, n):
            print(i, j, a_function(i, j))


def what_prob(i, j):
    if i < 0 or j < 0:
        return 0
    if j == i and i > 0:
        res = 0
        if a_function(i, i - 1) < 1:
            res += 1 - a_function(i, i - 1)
        if a_function(i, i + 1) < 1:
            res += 1 - a_function(i, i + 1)
        return res / 2
    if T(i, j) == 0:
        return 0
    aij = a_function(i, j)
    if aij >= 1:
        return 1 / 2
    return aij / 2


def print_prob(n):
    for i in range(0, n):
        for j in range(0, n):
            print(i, j, what_prob(i, j))


def run_chain(start, n):
    state = start
    for i in range(0, n):
        j_prev = what_prob(state, state - 1)
        j_same = what_prob(state, state)
        j_next = what_prob(state, state + 1)
        u = random.random()
        # print(u)
        if u < j_prev and state > 0:
            state = state - 1
        elif u < j_prev + j_same:
            state = state
        else:
            state = state + 1
    return state


def generate(number_of_intigers, length_of_chain):
    numbers = []
    for i in range(0, number_of_intigers):
        numbers.append(run_chain(0, length_of_chain))
    return numbers


def check(i, n, l):
    global lam
    lam = l

    y_points = np.random.poisson(lam, i)

    numbers = generate(i, n)
    maxx = 0
    for x in numbers:
        if x > maxx:
            maxx = x
    for x in y_points:
        if x > maxx:
            maxx = x
    freq = [0] * (maxx + 1)
    x_points = []
    for x in range(0, maxx + 1):
        x_points.append(x)
    for x in numbers:
        freq[x] = freq[x] + 1

    freq_org = [0] * (maxx + 1)
    for x in y_points:
        freq_org[x] = freq_org[x] + 1

    plt.plot(x_points, freq, label="generwoane")
    plt.plot(x_points, freq_org, label="modelowane")
    plt.legend()
    plt.title("Wystąpienia liczb generowanych zestawione z modelowymi")
    plt.show()

    mean = sum(numbers) / i
    print("wartość oczekiwana: ", mean, " a lambda była: ", lam)

    print(
        "Różnica bezwzględna (do 2 miejsc po przecinku) wygenerowanej ilości wystąpień danej liczby z teoretyczną (pi(i)), oraz błąd względny, ogólnie generujemy ",
        i,
        "liczb",
    )
    for x in x_points:
        print(
            x,
            format(abs((pi(x) * i) - freq[x]), ".2f"),
            format(abs((pi(x) * i) - freq[x]) / (pi(x) * i), ".2f"),
        )


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

    print("\nZadanie 3")
    print("lambda = 6")
    print("i", "j", "a(i,j):")
    print_a(10)
    print("i", "j", "prawdopodobieństwo X_n+1 = j | X_n = i:")
    print_prob(10)

    i = int(input("Podaj ilość liczb do wygenerowania (sugerowane >=800): "))
    n = int(input("Podaj długość łańcucha Markowa (sugerowane >=1000): "))
    l = int(input("Podaj lambdę(sugerowane 6 taka jak do obliczeń wyżej): "))
    print("cierpliwości...")
    check(i, n, l)
