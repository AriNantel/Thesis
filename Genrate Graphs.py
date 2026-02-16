import networkx as nx
import time
import matplotlib.pyplot as plt
from operator import itemgetter
import random
import pandas as pd

# Define the rate at which dryness increases
RHO = 0.05

'''def make_graph():
    nodes = ["A","B","C","D","E","F", "G", "H", "I", "J", "K", "L"]
    # Create edges between each vertex and the one next to it
    edges = list(zip(nodes, nodes[1:]))
    G = nx.Graph()
    G.add_edges_from(edges)
    # Hard code positions for the graph
    pos = {node: (i, 0) for i, node in enumerate(nodes)}
    # G = nx.connected_watts_strogatz_graph(15, 2, 0.2, tries=100, seed=None)

    return G, pos

def make_randome_graph():
    nodes = ["A","B","C","D","E","F", "G", "H", "I", "J", "K", "L"]
    G = nx.connected_watts_strogatz_graph(len(nodes), 3, 0.3, tries=100, seed=None)
    mapping = {i: nodes[i] for i in range(len(nodes))}
    G = nx.relabel_nodes(G, mapping)
    pos = nx.spring_layout(G)
    return G, pos'''

def makegraph(choice, parameter):
    #FROM MEGAN BRYSON
    #CHANGE SIZE AND GENERATION MODEL IN HERE!!
    
    #G = nx.Graph()
    #set graph size and type. type variable is only used in print/excel output later, not required for the alg to run
    graphsize = 30 #hard coded but you can change it here

    #choice = 3 #this is hard coded to use option 3, you can change this and also add different generation models from the ones networks has. the only thing is for the excel output you will probably want to set the type variables.
    #for graphs that arent always connected, you can set while loop to make them always connected IF YOU WANT
    if choice == 1:
        graphtype = "watts strogatz"
        #parameter = 0.2
        G = nx.connected_watts_strogatz_graph(graphsize, 9, parameter, seed=None)
        
    elif choice == 2:
         graphtype = "pa barbasi albert"
         #parameter = graphsize//5
         G = nx.barabasi_albert_graph(graphsize, parameter)
         while nx.is_connected(G) == False:
             G = nx.barabasi_albert_graph(graphsize, parameter)
    elif choice == 3:
        graphtype = "GNP"
        #parameter = 0.3
        G = nx.erdos_renyi_graph(graphsize, parameter)
        while nx.is_connected(G) == False:
            G = nx.erdos_renyi_graph(graphsize, parameter)
    else:
        graphtype = "Duplication–Divergence"
        #parameter = 0.4
        G = nx.duplication_divergence_graph(graphsize, parameter)
        while nx.is_connected(G) == False:
            G = nx.duplication_divergence_graph(graphsize, parameter)
             
  
    for i in range(graphsize):
        G.add_node(i)
    
    pos = nx.spring_layout(G, seed = 100) #sets location for nodes in the plot for viz, dont bothering changing this 
    
    # draw(G, pos)
    return G, pos, graphsize, graphtype, parameter

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


def run_alg(G, pos):
    #plt.ion()
    #fig = plt.figure()

    # Select the dryest vertex as the seed
    initial_node = start_node(G)
    #print(f"Initial node: {initial_node}")

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
                G.nodes[node]["dryness"] += RHO * num_burning
        
        for node in burned_this_round:
            not_burned.remove(node)
            G.nodes[node]["state"] = "burning"
            G.nodes[node]["color"] = "red"
        
        round += 1
    
    return round, initial_node


# FROM MEGAN BRYSON'S CODE FOR RUNNING MULTIPLE TESTS AND OUTPUTTING TO EXCEL

"""def generate_adjlist_with_all_edges(G, delimiter=" "):
    #COMMENT: adj list generator from stackoverflow
    
    for s, nbrs in G.adjacency():
        line = str(s) + delimiter
        for t, data in nbrs.items():
            line += str(t) + delimiter
        yield line[: -len(delimiter)]"""
        
def main():
    
    for run_id in range (0,10):
        G, pos, graphsize, graphtype, parameter = makegraph(4, 0.8) #edit these in makegraph()
        G = intital_nodes(G)
        
        testsnum = 50 #how many tests are we doing rn? can be increased here
        
        """adjlist = []
        for line in generate_adjlist_with_all_edges(G):
            tempadj = line.split()
            adjlist.append(tempadj)"""
        #print (adjlist)
        draw(G, pos)
        
        datadict = {}
        datalist =["testnumber", "parameter", "graphsize", "graphtype","nx.density(G)", "nx,average_clustering(G)", "nx.eccentricity(G,starting_node)","steps"]
        
        
        for i in range (testsnum):
            #steps, total, greennum = run_alg(G, pos)
            G = intital_nodes(G)
            steps,start_node = run_alg(G, pos)
            templist = [i, parameter, graphsize, graphtype,nx.density(G), nx.average_clustering(G), nx.eccentricity(G, start_node), steps]
            datadict [i] = templist
            

        pf = pd.DataFrame.from_dict(datadict, orient="index", columns= datalist)
        
        pf.transpose()


        #name can be changed of the sheets and file
        #with pd.ExcelWriter('Wildfire_Burning_Alg.xlsx', engine='openpyxl', mode='w') as writer: 
        with pd.ExcelWriter('Wildfire_Burning_Alg.xlsx', engine='openpyxl', mode='a', if_sheet_exists="new") as writer: #copilot generated comment: Open an Excel writer in append mode
            wb = writer.book  #copilot generated comment: Access the Excel workbook object
            ws = wb.active  #copilot generated comment: Access the active worksheet
            pf.to_excel(writer, sheet_name= graphtype + "p" + str(parameter) + "_" + str(run_id), index=False)  #copilot generated comment: Write the DataFrame to the Excel sheet named "DD"
    
main()
print("done")
      