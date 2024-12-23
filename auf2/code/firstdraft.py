#Description: die input Funktion für die Labyrinthe ohne Gruben; Dabei ist ein feld mit einer 0 ein Feld ohne Wand rechts und unten,
#1 mit Wand rechts, ein Feld 2 mit Wand unten, ein Feld 3 mit Wand unten und rechts.
def input_ohne_gruben(filename: str):
    matrizen = []
    with open(filename, 'r') as f:
        #Höhe m und Breite n der Matrix
        n,m = f.readline().split()
        n,m = int(n), int(m)
        for x in range(2):
            matrix = []
            for line in range(m):
                new_line = []
                for element in f.readline().split():
                    if element == '0':
                        new_line.append(0)
                    else:
                        new_line.append(1)
                new_line.append(1)
                matrix.append(new_line)
            for line in range(m-1):
                current_line = f.readline().split()
                for index in range(n):
                    if current_line[index] == 1:
                        if matrix[line+1][index] == 0:
                            matrix[line+1][index] = 2
                        else:
                            matrix[line+1][index] = 3
            for i in range(int(f.readline().split()[0])):
                f.readline()
                pass
            matrizen.append(matrix)
    return matrizen, m, n

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
            new_line=[]
            for i in range(2*n+1):
                new_line.append("# ")
            matrix.append(new_line)
            matrix.insert(0, new_line)
            matrizen.append(matrix)
    return matrizen, m, n

output = binary_maze("auf2/data/labyrinthe1.txt")
for line in output[0][0]:
    print("".join(line))