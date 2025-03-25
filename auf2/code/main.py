import os
import time
from datetime import datetime
import argparse
import heapq

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
    
    def neighbors(self, u):
        return self.graph[u]
    
    def add_grube(self, x, y):
        vertex = y*self.breite + x
        self.gruben.add(vertex)

    def delete_edges(self, u):
        self.graph[u] = []
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
    
    def length(self):
        return len(self.queue)

class PrioQueue:
    def __init__(self, height, width):
        self.queue = []
        self.height = height
        self.width = width



    def is_empty(self):
        return len(self.queue) == 0

    def length(self):
        return len(self.queue)
    #tuple mit state und max manhattan distance
    def push(self, data: tuple[tuple, int]):
        # Use (priority, state) structure for heapq
        heapq.heappush(self.queue, data)

    # Pop the element with the smallest priority (self.queue[i][1])
    def pop(self):
        # heapq.heappop() will return (priority, state), so we return only the state
        return heapq.heappop(self.queue)[1]

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

    pass
    #first check feasibility (bfs on both graphs independently)

    # check for independent subgraphs
    # check for bridges to independent subgraphs  

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
            if not (new_n1 in g1_gruben and new_n2 in g2_gruben):
                result.append(((new_n1, new_n2), d))

    return result

def manhattan_distance(node, height, width) -> int:
    x_n = node%width
    y_n = node//height
    return abs(x_n-width+1)+abs(y_n-height+1)

def max_heuristic(node1, node2, height, width, source_cost) -> int:
    return max(manhattan_distance(node1, height, width)+source_cost+1, manhattan_distance(node2, height, width)+source_cost+1)

def sum_heuristic(node1, node2, height, width, source_cost) -> int:
    return manhattan_distance(node1, height, width)+manhattan_distance(node2, height, width)+source_cost+1

def bfs_shortest_path(G1: Graph, destination: int) -> bool:
    visited = set()
    q = Queue()
    q.push(0)
    
    while not q.is_empty():
        vertex = q.pop()
        for neighbor in G1.neighbors(vertex):
            if neighbor in G1.gruben:
                visited.add(neighbor)
            else:
                if neighbor == destination:
                    return True
                if neighbor not in visited:
                    visited.add(neighbor)
                    q.push(neighbor)
    return False

def unidirectional_bfs(G1: Graph, G2: Graph, source: int, destination: int) -> tuple[dict, float]:
    start = time.time()
    # Value DS: (n1, n2): Tuple
    visited = set()
    # Value DS: ((prev_n1, prev_n2), direction): Tuple
    parent = {}
    q = Queue()

    q.push(source)
    visited.add(source)

    G1.delete_edges(destination[0])
    G2.delete_edges(destination[0])

    while not q.is_empty():
        current_vertex = q.pop()
        if current_vertex == destination:
            break

        for neighbor in graph_product(G1, G2, current_vertex, G1.gruben, G2.gruben):
            if neighbor[0] not in visited:
                parent[neighbor[0]] = (current_vertex, neighbor[1])
                q.push(neighbor[0])
                visited.add(neighbor[0])
    end = time.time()
    return parent, end-start

def bidirectional_bfs(G1: Graph, G2: Graph, source: int, destination: int) -> list[tuple[list, list], int, float]:
    start = time.time()
    q_start = Queue()
    q_end = Queue()
    visited_start = set()
    visited_end = set()
    parent_start = {}
    parent_end = {}


    q_start.push(source)
    q_end.push(destination)

    visited_start.add(source)
    visited_end.add(destination)

    break_condition = False

    while not q_start.is_empty() and not q_end.is_empty():
        if break_condition == True:
            break
        if q_start.length() < q_end.length():
            root_vertex = q_start.pop()
            for neighbor in graph_product(G1, G2, root_vertex, G1.gruben, G2.gruben):
                if neighbor[0] not in visited_start:
                    parent_start[neighbor[0]] = (root_vertex, neighbor[1])
                    if neighbor[0] in visited_end:
                        meeting_vertex = neighbor[0]
                        break_condition = True
                        break

                    q_start.push(neighbor[0])
                    visited_start.add(neighbor[0])
        else:
            root_vertex = q_end.pop()
            for neighbor in graph_product(G1, G2, root_vertex, G1.gruben, G2.gruben):
                if neighbor[0] not in visited_end:
                    parent_end[neighbor[0]] = (root_vertex, neighbor[1])
                    if neighbor[0] in visited_start:
                        meeting_vertex = neighbor[0]
                        break_condition = True
                        break
                    q_end.push(neighbor[0])
                    visited_end.add(neighbor[0])

    end = time.time()
    return (parent_start, parent_end), meeting_vertex, end-start

def unidirectional_a_star(G1: Graph, G2: Graph, source: tuple, destination: tuple, height: int, width: int):
    start = time.time()

    q = PrioQueue(height, width)
    q.push((manhattan_distance(0, height, width), source))

    visited = set()
    parent = {} 
    cost = {}
    cost[source] = 0
    visited.add(source)

    G1.delete_edges(destination[0])
    G2.delete_edges(destination[0])
    while not q.is_empty():
        current_vertex = q.pop()
        source_cost = cost[current_vertex]

        if current_vertex == destination:
            break

        for neighbor in graph_product(G1, G2, current_vertex, G1.gruben, G2.gruben):
            if neighbor[0] not in visited:
                parent[neighbor[0]] = (current_vertex, neighbor[1])
                cost[neighbor[0]] = source_cost + 1
                q.push((max_heuristic(neighbor[0][0], neighbor[0][1], height, width, source_cost), neighbor[0]))
                visited.add(neighbor[0])
    end = time.time()
    return parent, end-start

def uni_a_star_sum(G1: Graph, G2: Graph, source: tuple, destination: tuple, height: int, width: int):
    start = time.time()

    q = PrioQueue(height, width)
    q.push((sum_heuristic(0,0,height, width, 0), source))

    visited = set()
    parent = {} 
    cost = {}
    cost[source] = 0
    visited.add(source)

    G1.delete_edges(destination[0])
    G2.delete_edges(destination[0])

    while not q.is_empty():
        current_vertex = q.pop()
        source_cost = cost[current_vertex]

        if current_vertex == destination:
            break

        for neighbor in graph_product(G1, G2, current_vertex, G1.gruben, G2.gruben):
            if neighbor[0] not in visited:
                parent[neighbor[0]] = (current_vertex, neighbor[1])
                cost[neighbor[0]] = source_cost + 1
                q.push((sum_heuristic(neighbor[0][0], neighbor[0][1], height, width, source_cost), neighbor[0]))
                visited.add(neighbor[0])
    end = time.time()
    return parent, end-start

def bidirectional_sequence(parent_start: list, parent_end: list, meeting_vertex: int, destination: int) -> list:
    path = []
    directions = {
        "U": "D",
        "D": "U",
        "L": "R",
        "R": "L"
    }
    current_vertex = meeting_vertex
    while current_vertex != (destination, destination):
        path.append(directions[parent_end[current_vertex][1]])
        current_vertex = parent_end[current_vertex][0]
    path = path[::-1]
    current_vertex = meeting_vertex
    while current_vertex != (0,0):
        path.append(parent_start[current_vertex][1])
        current_vertex = parent_start[current_vertex][0]
    path = path[::-1]

    return path

def unidirectional_sequence(parent: dict, destination: int) -> list:
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
        f.write("Runtime for creating the graphs: " + str(graph_time)[0:8] + " s\n")
        f.write("Runtime for running BFS on product graph: " + str(bfs_time)[0:8] + " s\n\n")
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

def run_presolving():
    for _ in range(10):
        current = os.getcwd() + "/auf2/output/presolving/"
        print(f"Working on file {_}")
        filename = f"./auf2/data/labyrinthe{_}.txt"
        g1, g2, hoehe, breite, graph_time = graphen_erstellen(filename)
        dest = hoehe*breite-1
        if bfs_shortest_path(g1, dest) and bfs_shortest_path(g2, dest):
            with open(current + filename.split("/")[-1][-5] + ".txt", 'w') as f:
                f.write("Solvable")
        else:
            with open(current + filename.split("/")[-1][-5] + ".txt", 'w') as f:
                f.write("Impossible to complete. No continuous flow in one of the mazes.\nNo solution found.")

def run_unidirectional_bfs():
    current = os.getcwd() + "/auf2/output/"
    folder_path = os.path.join(current, str(datetime.now().strftime("%m-%d_%H-%M_unidir"))) + "/"
    os.makedirs(folder_path, exist_ok=True)
    input_files = map(int,input("Welche Dateien sollen getestet werden? Nummern mit Leerzeichen trennen: ").split())
    for _ in input_files:
        print(f"Working on file {_}")
        filename = f"./auf2/data/labyrinthe{_}.txt"
        g1, g2, hoehe, breite, graph_time = graphen_erstellen(filename)
        dest = hoehe*breite-1
        if bfs_shortest_path(g1, dest) and bfs_shortest_path(g2, dest):
            parentlist, bfs_time = unidirectional_bfs(g1, g2, (0,0), (dest,dest))
            path = unidirectional_sequence(parentlist, (dest,dest))
            write_to_file(path, graph_time, bfs_time, "solution" + filename.split("/")[-1][-5] + ".txt", folder_path)
        else:
            with open(folder_path + "solution" + filename.split("/")[-1][-5] + ".txt", 'w') as f:
                f.write("Impossible to complete. No continuous flow in one of the mazes.\nNo solution found.")

def run_bidirectional_bfs():
    current = os.getcwd() + "/auf2/output/"
    folder_path = os.path.join(current, str(datetime.now().strftime("%m-%d_%H-%M_bidir"))) + "/"
    os.makedirs(folder_path, exist_ok=True)
    input_files = map(int,input("Welche Dateien sollen getestet werden? Nummern mit Leerzeichen trennen: ").split())
    for _ in input_files:
        print(f"Working on file {_}")
        filename = f"./auf2/data/labyrinthe{_}.txt"
        g1, g2, hoehe, breite, graph_time = graphen_erstellen(filename)
        dest = hoehe*breite-1
        if bfs_shortest_path(g1, dest) and bfs_shortest_path(g2, dest):
            parentlists, meeting_vertex, bfs_time = bidirectional_bfs(g1, g2, (0,0), (dest,dest))
            path = bidirectional_sequence(parentlists[0], parentlists[1], meeting_vertex, dest) 
            write_to_file(path, graph_time, bfs_time, "solution" + filename.split("/")[-1][-5] + ".txt", folder_path)
        else:
            with open(folder_path + "solution" + filename.split("/")[-1][-5] + ".txt", 'w') as f:
                f.write("Impossible to complete. No continuous flow in one of the mazes.\nNo solution found.")

def run_astar():
    current = os.getcwd() + "/auf2/output/"
    folder_path = os.path.join(current, str(datetime.now().strftime("%m-%d_%H-%M_astar"))) + "/"
    os.makedirs(folder_path, exist_ok=True)
    input_files = map(int,input("Welche Dateien sollen getestet werden? Nummern mit Leerzeichen trennen: ").split())
    for _ in input_files:
        print(f"Working on file {_}")
        filename = f"./auf2/data/labyrinthe{_}.txt"
        g1, g2, hoehe, breite, graph_time = graphen_erstellen(filename)
        dest = hoehe*breite-1
        if bfs_shortest_path(g1, dest) and bfs_shortest_path(g2, dest):
            parentlists, bfs_time = unidirectional_a_star(g1, g2, (0,0), (dest,dest), breite, hoehe)
            path = unidirectional_sequence(parentlists, (dest,dest)) 
            write_to_file(path, graph_time, bfs_time, "solution" + filename.split("/")[-1][-5] + ".txt", folder_path)
        else:
            with open(folder_path + "solution" + filename.split("/")[-1][-5] + ".txt", 'w') as f:
                f.write("Impossible to complete. No continuous flow in one of the mazes.\nNo solution found.")

def run_astar_sum():
    current = os.getcwd() + "/auf2/output/"
    folder_path = os.path.join(current, str(datetime.now().strftime("%m-%d_%H-%M_astar"))) + "/"
    os.makedirs(folder_path, exist_ok=True)
    input_files = map(int,input("Welche Dateien sollen getestet werden? Nummern mit Leerzeichen trennen: ").split())
    for _ in input_files:
        print(f"Working on file {_}")
        filename = f"./auf2/data/labyrinthe{_}.txt"
        g1, g2, hoehe, breite, graph_time = graphen_erstellen(filename)
        dest = hoehe*breite-1
        if bfs_shortest_path(g1, dest) and bfs_shortest_path(g2, dest):
            parentlists, bfs_time = uni_a_star_sum(g1, g2, (0,0), (dest,dest), breite, hoehe)
            path = unidirectional_sequence(parentlists, (dest,dest)) 
            write_to_file(path, graph_time, bfs_time, "solution" + filename.split("/")[-1][-5] + ".txt", folder_path)
        else:
            with open(folder_path + "solution" + filename.split("/")[-1][-5] + ".txt", 'w') as f:
                f.write("Impossible to complete. No continuous flow in one of the mazes.\nNo solution found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run BFS algorithms based on the provided flag.")
    # Define the flag -u for unidirectional BFS
    parser.add_argument('-u', '--unidirectional', action='store_true', help='Run unidirectional BFS')
    # Define the flag -b for bidirectional BFS
    parser.add_argument('-b', '--bidirectional', action='store_true', help='Run bidirectional BFS')

    parser.add_argument('-a', '--astar', action='store_true', help='Run A-Star Algorithm')

    parser.add_argument('-s', '--astar_sum', action='store_true', help='Run A-Star Algorithm with Sum Heuristic')
    
    args = parser.parse_args()

    if args.unidirectional:
        run_unidirectional_bfs()
    elif args.bidirectional:
        run_bidirectional_bfs()
    elif args.astar:
        run_astar()
    elif args.astar_sum:
        run_astar_sum()
    else:
        print("No valid flag provided. Use -u, -b, -a, -s to run the respective algorithms.")