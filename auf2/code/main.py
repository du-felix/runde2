import os
import time
from datetime import datetime
class Graph:
    def __init__(self, hoehe, breite):
        self.breite = breite
        self.hoehe = hoehe
        self.V = hoehe * breite
        self.graph = {x: [] for x in range(self.V)}
        self.gruben = set([])

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def edge_exists(self, u, v):
        if v in self.graph[u]:
            return True
        return False
    
    def edge_direction(self, u, d):
        if d == "U":
            if self.edge_exists(u, u - self.breite):
                return u - self.breite
            return u
        elif d == "D":
            if self.edge_exists(u, u + self.breite):
                return u + self.breite
            return u
        elif d == "L":
            if self.edge_exists(u, u - 1):
                return u - 1
            return u
        elif d == "R":
            if self.edge_exists(u, u + 1):
                return u + 1
            return u

    def edge_count(self):
        val = 0 - self.gruben
        for keys, values in self.graph.items():
            val += len(values)
        return val // 2
    
    def get_adj_nodes(self, u):
        return self.graph[u]
    
    def add_grube(self, x, y):
        vertex = y*self.breite + x
        self.gruben.add(vertex)
class Queue:
    def __init__(self):
        self.queue = []

    def get(self):
        return self.queue

    def push(self, x):
        self.queue.append(x)

    def pop(self):
        return self.queue.pop(0)
    
    def is_empty(self):
        return len(self.queue) == 0

def graph_product(G1: Graph, G2: Graph, root: tuple, g1_gruben, g2_gruben) -> list[(int, int)]:
    directions = ["U", "D", "L", "R"]
    result = []
    n1, n2 = root
    for d in directions:
        new_n1 = G1.edge_direction(n1, d)
        new_n2 = G2.edge_direction(n2, d)
        if new_n1 != n1 or new_n2 != n2:
            if new_n1 in g1_gruben:
                new_n1 = 0
            if new_n2 in g2_gruben:
                new_n2 = 0
            result.append(((new_n1, new_n2), d))

    return result

def graphen_erstellen(filename) -> list[Graph, Graph, int, int]:
    start = time.time()
    with open(filename, "r") as f:
        #Variablen Initialisieren
        breite, hoehe = map(int, f.readline().split())
        G1 = Graph(hoehe, breite)
        G2 = Graph(hoehe, breite)

        for G in [G1, G2]:
            for x in range(hoehe):
                line = f.readline().strip().split()
                for y in range(breite-1):
                    if line[y] == "0":
                        G.add_edge(x * breite + y, x * breite + y + 1)
            
            for x in range(hoehe-1):
                line = f.readline().strip().split()
                for y in range(breite):
                    if line[y] == "0":
                        G.add_edge(x * breite + y, (x + 1) * breite + y)
            
            for x in range(int(f.readline().strip())):
                line = f.readline().strip().split()
                G.add_grube(int(line[0]), int(line[1]))
    end = time.time()
    return (G1, G2, hoehe, breite, end-start)

def graph_optimieren(G):
    pass
    # check for independent subgraphs
    # check for bridges to independent subgraphs  

def bfs(G1: Graph, G2: Graph, source: int, destination: int) -> tuple[dict, float]:
    start = time.time()
    # Value DS: (n1, n2): Tuple
    visited = set()
    # Value DS: ((prev_n1, prev_n2), direction): Tuple
    parent = {}
    q = Queue()

    q.push(source)
    visited.add(source)

    while not q.is_empty():
        root_vertex = q.pop()

        if root_vertex == destination:
            break

        for neighbor in graph_product(G1, G2, root_vertex, G1.gruben, G2.gruben):
            if neighbor[0] not in visited:
                parent[neighbor[0]] = (root_vertex, neighbor[1])
                q.push(neighbor[0])
                visited.add(neighbor[0])
    end = time.time()
    return parent, end-start

def get_command_sequence(parent: dict, destination: int) -> list:
    if parent.get(destination) == None:
        return []
    else:
        path = []
        current_vertex = destination
        while current_vertex != (0,0):
            path.append(parent[current_vertex][1])
            current_vertex = parent[current_vertex][0]
        


        return path[::-1]
    
def print_path(path: list):
    if path == []:
        print("Es existiert keine Folge von Anweisungen, um zum Ziel zu gelangen.")
    else:
        print("Folgende Anweisungen sollen ausgeführt werden: ")
        for index, p in enumerate(path, start=1):
            if p == "U":
                print(index, "Oben")
            elif p == "D":
                print(index, "Unten")
            elif p == "L":
                print(index, "Links")
            elif p == "R":
                print(index, "Rechts")

def write_to_file(path, graph_time, bfs_time, data, folder_path):
    with open(folder_path + data, 'w') as f:
        f.write("Runtime for creating the graphs: " + str(graph_time)[0:6] + " s\n")
        f.write("Runtime for running BFS on product graph: " + str(bfs_time)[0:6] + " s\n\n")
        if path != []:
            for index, p in enumerate(path, start=1):
                if p == "U":
                    f.write(str(index) + " " + "Oben" + "\n")
                elif p == "D":
                    f.write(str(index) + " " + "Unten" + "\n")
                elif p == "L":
                    f.write(str(index) + " " + "Links" + "\n")
                elif p == "R":
                    f.write(str(index) + " " + "Rechts" + "\n")
        else:
            f.write("No solution found...")

if __name__ == "__main__":
    current = os.getcwd() + "/auf2/output/"
    folder_path = os.path.join(current, str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))) + "/"
    os.makedirs(folder_path, exist_ok=True)
    for _ in [0,1,2,3,7,4,8,5,9,6]:
        print(f"Working on file {_}")
        filename = f"./auf2/data/labyrinthe{_}.txt"
        g1, g2, hoehe, breite, graph_time = graphen_erstellen(filename)
        parentlist, bfs_time = bfs(g1, g2, (0,0), (hoehe*breite-1, hoehe*breite-1))
        path = get_command_sequence(parentlist, (hoehe*breite-1, hoehe*breite-1))
        write_to_file(path, graph_time, bfs_time, "solution" + filename.split("/")[-1][-5] + ".txt", folder_path)
        