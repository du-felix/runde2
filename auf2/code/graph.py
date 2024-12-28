import pulp as pl
import networkx as nx
import  matplotlib.pyplot as plt
import time as t

class Graph:
    def __init__(self):
        self.graph = {}
        self.edges = []
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)
    def add_edge(self, u, v):
        self.edges.append((u,v))
        self.edges.append((v,u))
#Breite n, Höhe m
#Source: 0, Destination: m*n-1
#0 = Add Edge, 1 = Wand
#Erstmal nur für ein Labyrinth
def get_graph(filename):
    with open(filename, "r") as f:
        #n, m lesen
        n,m = f.readline().split()
        n,m = int(n), int(m)

        #Initialize Graph Nodes
        G = nx.Graph()
        for i in range(m*n):
            G.add_node(i)

        #Alle horizontalen Kanten
        for lines in range(m):
            current_line = f.readline().split()
            for index in range(n-1):
                element = int(current_line[index])
                if int(element) == 0:
                    source_node = lines*n+index
                    destination_node = lines*n+index+1
                    G.add_edge(source_node, destination_node)
                    #G.add_edge(destination_node, source_node)
                else:
                    pass
        
        #Alle vertikalen Kanten
        for lines in range(m-1):
            current_line = f.readline().split()
            for index in range(n):
                element = int(current_line[index])
                if int(element) == 0:
                    source_node = lines*n+index
                    destination_node = (lines+1)*n+index
                    G.add_edge(source_node, destination_node)
                    #G.add_edge(destination_node, source_node)
                else:
                    pass
    return G, n, m

def get_graph_own_class(filename):
    with open(filename, "r") as f:
        #n, m lesen
        n,m = f.readline().split()
        n,m = int(n), int(m)

        #Initialize Graph Nodes
        G = Graph()
        for i in range(m*n):
            G.add_node(i)

        #Alle horizontalen Kanten
        for lines in range(m):
            current_line = f.readline().split()
            for index in range(n-1):
                element = int(current_line[index])
                if int(element) == 0:
                    source_node = lines*n+index
                    destination_node = lines*n+index+1
                    G.add_edge(source_node, destination_node)
                else:
                    pass
        
        #Alle vertikalen Kanten
        for lines in range(m-1):
            current_line = f.readline().split()
            for index in range(n):
                element = int(current_line[index])
                if int(element) == 0:
                    source_node = lines*n+index
                    destination_node = (lines+1)*n+index
                    G.add_edge(source_node, destination_node)
                else:
                    pass
    return G, n, m


G, n, m = get_graph("./auf2/data/laby0_short2.txt")

nodes = list(G.nodes)
edges = list(G.edges)

source = 0
destination = n * m - 1

problem = pl.LpProblem("Shortest Path Problem", pl.LpMinimize)
edge_vars = {edge: pl.LpVariable(f"x_{edge[0]}_{edge[1]}", cat="Binary") for edge in edges}

# Objective: Minimize the number of edges selected (can also be weighted)
problem += pl.lpSum([edge_vars[edge] for edge in edges])

# constraints

# Source Node muss für eine Kante ausgehend sein
problem += pl.lpSum([edge_vars[edge] for edge in edges if edge[0] == source]) == 1
# Destination Node muss für eine Kante eingehend sein
problem += pl.lpSum([edge_vars[edge] for edge in edges if edge[1] == destination]) == 1

# Outgoing - Incoming = 0 für alle Knoten, außer Source und Destination
for node in nodes:
    if node == source or node == destination:
        continue
    else:
        problem += (pl.lpSum([edge_vars[edge] for edge in edges if edge[1] == node]) - pl.lpSum([edge_vars[edge] for edge in edges if edge[0] == node]) == 0,f"Flow_Conservation_{node}")

# Solve the problem
status = problem.solve()

def print_sol():
    # Display the solver status
    print(f"Solver Status: {pl.LpStatus[problem.status]}")

    # Check if the solution is optimal

    # Retrieve the values of edge variables
    for edge, var in edge_vars.items():
        print(f"Edge {edge}: Used = {var.varValue}")

    for edge, var in edge_vars.items():
        if var.varValue == 1:
            print(edge)

    # Retrieve the optimal objective value
    print(f"\nOptimal Total Cost: {float(len(edges)) - pl.value(problem.objective)}")

print_sol()

# Print all constraints
while False:
    for name, constraint in problem.constraints.items():
        print(f"{name}: {constraint}")