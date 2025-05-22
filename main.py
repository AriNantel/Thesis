import networkx as nx
import matplotlib.pyplot as plt
import random

nodes = ["A","B","C","D","E","F"]
edges = list(zip(nodes, nodes[1:]))
G = nx.Graph()
G.add_edges_from(edges)
pos = {node: (i, 0) for i, node in enumerate(nodes)}

for node in G.nodes:
    G.nodes[node]["color"] = "blue"
    G.nodes[node]["state"] = "safe"

initial_node = random.choice(list(G.nodes))
G.nodes[initial_node]["color"] = "red"
G.nodes[initial_node]["state"] = "safe"
burned = [initial_node]

plt.ion()
fig = plt.figure()

def draw(step):
    plt.clf()
    colors = [G.nodes[n]["color"] for n in G.nodes]
    nx.draw(G, pos=pos, with_labels=True, node_color=colors)
    plt.title(f"Step {step}")
    plt.pause(1)

draw(0)

step = 1
while burned:
    new_burning = []
    for node in burned:
        for neighbor in G.neighbors(node):
            if G.nodes[neighbor]["state"] == "safe":
                G.nodes[neighbor]["state"] = "burning"
                G.nodes[neighbor]["color"] = "red"
                new_burning.append(neighbor)

    burned = new_burning
    draw(step)
    step += 1

# End interactive mode
plt.ioff()
plt.show()
