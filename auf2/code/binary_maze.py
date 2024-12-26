#Das generierte Labyrinth generiert für jedes Feld aus der Originaleingabe, zwei Felder, eins für das Feld, das andere, um die Wände zu speichern.
#Somit entsprechen zwei Schritte im Labyrinth einem Schritt in der Originaleingabe. 
def binary_maze(filename: str) -> list[list, int, int]:
    matrizen = []
    with open(filename, "r") as f:
        n,m = f.readline().split()
        n,m = int(n), int(m)
        for x in range(2):
            matrix  = []
            for lines in range(m):
                new_line = ["# "]
                for element in f.readline().split():
                    if int(element) == 0:
                        new_line.append("  ")
                        new_line.append("  ")
                    else:
                        new_line.append("  ")
                        new_line.append("# ")
                new_line.append("  ")
                new_line.append("# ")
                matrix.append(new_line)
            for line in range(m-1):
                current_input = f.readline().split()
                for index in range(1,n+1):
                    if current_input[index-1] == 1 and matrix[line+1][2*index-1] == "  ":
                        matrix[line+1][2*index-1] = "# "

            #Gruben werden ignoriert
            for i in range(int(f.readline().split()[0])):
                f.readline()
                pass
            matrix[0][1] = "S "
            matrix[-1][-2] = "X "
            new_line=[]
            for i in range(2*n+1):
                new_line.append("# ")
            matrix.append(new_line)
            matrix.insert(0, new_line)
            matrizen.append(matrix)
    return matrizen, m, n

def print_maze(output: list[list, int, int]):
    print("Matrix 1")
    for line in output[0][0]:
        print("".join(line))
    print("Matrix 2")
    for line in output[0][1]:
        print("".join(line))
    return 0

#Eventuell später auch mit Backtracking implementierbar. Wäre gut als Vergleich der Laufzeiten.
def bfs_shortest_path(maze, m, n) -> list[list, int]:
    pass

print_maze(binary_maze("auf2/data/labyrinthe6.txt"))
