import pulp as pl
import networkx as nx
import  matplotlib.pyplot as plt
import time as t

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

G, n, m = get_graph("./auf2/data/labyrinthe0.txt")

nodes = list(G.nodes())
edges = list(G.edges())
M=len(nodes)

source = 0
destination = n * m - 1

problem = pl.LpProblem("Shortest Path Problem", pl.LpMinimize)
edge_vars = {edge: pl.LpVariable(f"x_{edge[0]}_{edge[1]}", cat="Binary") for edge in edges}
# Position variables for each node (integer variables)
position_vars = {i: pl.LpVariable(f"p_{i}", lowBound=0, upBound=n-1, cat="Integer") for i in nodes}

# Objective: Minimize the number of edges selected (can also be weighted)
problem += pl.lpSum([edge_vars[edge] for edge in edges])

# Position constraints (ensuring the path is continuous)
for (i, j) in edges:
    # Ensuring that p[j] is one greater than p[i] if edge (i, j) is used
    problem += position_vars[j] >= position_vars[i] + 1 - M * (1 - edge_vars[(i, j)]), f"Position_Constraint_{i}_{j}"
    # Ensuring that p[i] is one greater than p[j] if edge (j, i) is used
    problem += position_vars[i] >= position_vars[j] + 1 - M * (1 - edge_vars[(i, j)]), f"Position_Constraint_{j}_{i}"

# Source node must be at position 0
problem += position_vars[source] == 0, "Source_Position"

# Destination node must be at position n-1
problem += position_vars[destination] == n-1, "Destination_Position"

# Source Node muss für eine Kante ausgehend sein
#problem += pl.lpSum([edge_vars[edge] for edge in edges if edge[0] == source]) == 1
# Destination Node muss für eine Kante eingehend sein
#problem += pl.lpSum([edge_vars[edge] for edge in edges if edge[1] == destination]) == 1

# Outgoing - Incoming = 0 für alle Knoten, außer Source und Destination
for node in nodes:
    if node == source or node == destination:
        continue
    else:
        problem += (pl.lpSum([edge_vars[edge] for edge in edges if edge[0] == node or edge[1] == node]) - pl.lpSum([edge_vars[edge] for edge in edges if edge[1] == node or edge[0] == node]) == 0,f"Flow_Conservation_{node}")

# Solve the problem
status = problem.solve()

# Objective Function
# Extract the results
if pl.LpStatus[problem.status] == "Optimal":
    print("Optimal Path Found:")
    selected_edges = [(i, j) for (i, j) in edges if pl.value(edge_vars[(i, j)]) == 1]
    print("Selected Edges:", selected_edges)
    
    # Also print the positions of the nodes in the path
    for node in nodes:
        print(f"Node {node} is at position {pl.value(position_vars[node])}")
else:
    print("No optimal solution found.")

while False:
    # Display the solver status
    print(f"Solver Status: {pl.LpStatus[problem.status]}")

    # Check if the solution is optimal
    if pl.LpStatus[problem.status] == "Optimal":
        print("\nOptimal Solution Found:")
        
        # Retrieve the values of edge variables
        for edge, var in edge_vars.items():
            print(f"Edge {edge}: Used = {var.varValue}")
        
        # Retrieve the optimal objective value
        print(f"\nOptimal Total Cost: {pl.value(problem.objective)}")
    else:
        print("No optimal solution found.")

# Print all constraints
while False:
    for name, constraint in problem.constraints.items():
        print(f"{name}: {constraint}")