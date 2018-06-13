import score
import networkx
import numpy as np
import matplotlib.pyplot as plt

def random_init_hubs(n: int):
    hubs = []
    while True:
        randint = np.random.randint(0, score.N)
        if randint in hubs:
            continue
        else:
            hubs.append(randint)
        if len(hubs) == n:
            break
    return np.asarray(hubs)


def replace(a: score.np.ndarray, olde, newe):
    newarray = a.copy()
    newarray[newarray == olde] = newe
    return newarray


def print_hubs(hubs: score.np.ndarray, owner: score.np.ndarray):
    for h in hubs:
        cities = np.where(owner == h)[0]
        print(f"{h}:{cities}")


def print_result(result):
    (hubs, owner), metrics = result
    n = len(hubs)
    print(f"{'*'*20} Solution for {n}-hub {'*'*20}")
    print(f"Find best result of:")
    print(f"Network Design:")
    print_hubs(hubs, owner)
    print(f"Metrics:")
    for k,v in metrics.items():
        print(f'  - {k}: {v}')
    print(f"{'*'*20} End {'*'*20}")


def choose_initial_hub(n: int):
    pair_distance = {}
    for i in range(0, score.N):
        for j in range(0, score.N):
            pair_distance[(i, j)] = score.D[i, j]
    sorted_pair_distance = sorted(pair_distance.items(), key=lambda x: x[1], reverse=True)
    hubs = []
    for (i, j), d in sorted_pair_distance:
        if i not in hubs:
            hubs.append(i)
            if len(hubs) == n:
                return hubs
        if j not in hubs:
            hubs.append(j)
            if len(hubs) == n:
                return hubs


def owned_by(h: int, owner: score.np.ndarray):
    return np.where(owner == h)[0]


def draw_network(owner: score.np.ndarray):
    g = networkx.Graph()
    hubs = list(set(owner.reshape([owner.size, ])))
    for h1 in hubs:
        for h2 in hubs:
            if h1 == h2:
                continue
            h1 = int(h1)
            h2 = int(h2)
            g.add_edge(h1, h2, weight=score.D[h1][h2])
    for h in hubs:
        cities = score.score.score.np.where(owner == h)[0]
        for c in cities:
            if c == h:
                continue
            h = int(h)
            c = int(c)
            g.add_edge(h, c, weight=score.D[h][c])
    plt.plot()
    networkx.draw_kamada_kawai(g,with_labels = True)
    print(g.edges())
    plt.show()