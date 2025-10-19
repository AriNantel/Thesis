import networkx as nx
import matplotlib.pyplot as plt
import random

def make_graph():
    nodes = ["A","B","C","D","E","F", "G", "H", "I", "J", "K", "L", "M"]
    # Create edges between each vertex and the one next to it
    edges = list(zip(nodes, nodes[1:]))
    G = nx.Graph()
    G.add_edges_from(edges)
    # Hard code positions for the graph
    pos = {node: (i, 0) for i, node in enumerate(nodes)}
    # G = nx.connected_watts_strogatz_graph(15, 2, 0.2, tries=100, seed=None)

    return G, pos

def initiate_nodes(G):
    # Colour all the nodes blue and set them as safe
    for node in G.nodes:
        G.nodes[node]["color"] = "blue"
        G.nodes[node]["state"] = "safe"
        G.nodes[node]["dryness"] = 0.9
    return G

def draw(G, pos):
    plt.clf()

    # Get the colors from node attributes
    colors = [G.nodes[n]["color"] for n in G.nodes]
    # Create labels showing both node name and dryness (rounded to 2 decimals)
    labels = {n: f"{n}\n{G.nodes[n]['dryness']:.2f}" for n in G.nodes}
    nx.draw(G, pos=pos, with_labels=True, labels=labels, node_color=colors, edgecolors="black", node_size=1000)
    plt.pause(1)

def start_node(G):
    initial_node = list(G.nodes)[0]
    for node in G.nodes:
        if G.nodes[node]["dryness"] > G.nodes[initial_node]["dryness"]:
            initial_node = node
    return initial_node

def num_burning_neighbors(G, node):
    count = 0
    for neighbor in G.neighbors(node):
        if G.nodes[neighbor]["state"] == "burning":
            count += 1
    return count


def main():
    plt.ion()
    fig = plt.figure()

    G, pos = make_graph()
    G = initiate_nodes(G)

    # Select the dryest vertex as the seed
    initial_node = list(G.nodes)[0]
    print(f"Initial node: {initial_node}")

    # Ignite the initial node
    G.nodes[initial_node]["color"] = "red"
    G.nodes[initial_node]["state"] = "burning"

    not_burned = list(G.nodes)
    not_burned.remove(initial_node)

    round = 0

    # While there are still nodes to infect
    while not_burned:
        burned_this_round = []

        for node in not_burned:
            num_neighbors = len(list(G.neighbors(node)))
            num_burning = num_burning_neighbors(G, node)
            
            
            if 1 - G.nodes[node]["dryness"] <= num_burning / num_neighbors:
            
                # Remove the selected neighbour from the list of available neighbours
                burned_this_round.append(node)

                
            else:
                G.nodes[node]["dryness"] += 0.05 * num_burning
        
        for node in burned_this_round:
            not_burned.remove(node)
            G.nodes[node]["state"] = "burning"
            G.nodes[node]["color"] = "red"
        
        round += 1
        
        draw(G, pos)
    print(f"All nodes burned in {round} rounds.")

    # End interactive mode
    plt.ioff()
    plt.show()

print("Running new algorithm")
main()