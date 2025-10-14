import networkx as nx
import matplotlib.pyplot as plt
import random

def make_graph():
    nodes = ["A","B","C","D","E","F"]
    # Create edges between each vertex and the one next to it
    edges = list(zip(nodes, nodes[1:]))
    G = nx.Graph()
    G.add_edges_from(edges)
    # Hard code positions for the graph
    pos = {node: (i, 0) for i, node in enumerate(nodes)}
    # G = nx.connected_watts_strogatz_graph(15, 2, 0.2, tries=100, seed=None)

    return G, pos

def intital_nodes(G):
    # Colour all the nodes blue and set them as safe
    for node in G.nodes:
        G.nodes[node]["color"] = "blue"
        G.nodes[node]["state"] = "safe"
        G.nodes[node]["dryness"] = random.uniform(0, 1)
    return G

def draw(G, pos):
    plt.clf()

    # Get the colors from node attributes
    colors = [G.nodes[n]["color"] for n in G.nodes]
    nx.draw(G, pos=pos, with_labels=True, node_color=colors)
    plt.pause(1)

def start_node(G):
    initial_node = list(G.nodes)[0]
    for node in G.nodes:
        if G.nodes[node]["dryness"] > initial_node["dryness"]:
            initial_node = node
    return initial_node


def main():
    plt.ion()
    fig = plt.figure()

    G, pos = make_graph()
    G = intital_nodes(G)

    # Select the dryest vertex as the seed
    initial_node = start_node(G)
    print(f"Initial node: {initial_node}")

    # Ignite the initial node
    G.nodes[initial_node]["color"] = "red"
    G.nodes[initial_node]["state"] = "burning"
    burning = [initial_node]

    # While there are still nodes to infect
    while infected:
        # List of nodes that have been infected this round
        infecting = []

        
        for node in infected:
            # For every infected node, if it was able to infect make it infected and change its color
            if G.nodes[node]["state"] == "infecting":
                G.nodes[node]["state"] = "infected"
                G.nodes[node]["color"] = "green"

                # Number of nodes that will be infected
                K = 1

                # Number of vertices that have been infected this round
                num_infected = 0

                # Get a list of all the neighbors of the infecting vertex
                neighbors = list(G.neighbors(node))

                # while we have infected less than K vertices and there are still available neighbours to check
                while num_infected < K and neighbors:

                    # Select at randome a neighbour to infect
                    infect = random.choice(neighbors)

                    # Remove the selected neighbour from the list of available neighbours
                    neighbors.remove(infect)

                    # If the selected node is safe infect it and add it to the list of infecting vertices
                    if G.nodes[infect]["state"] == "safe":
                        G.nodes[infect]["state"] = "infecting"
                        G.nodes[infect]["color"] = "red"
                        infecting.append(infect)
                        num_infected += 1
        # Set the list of infected vertices to the newly infecting nodes
        infected = infecting
        draw(G, pos)

    # End interactive mode
    plt.ioff()
    plt.show()

main()