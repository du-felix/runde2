from pyscipopt import Model

# -1 entspricht unbekannt bzw. undefiniert.
def create_binary_matrix(filename: str) -> list[list, int, int, list]:
    matrix = []
    with open(filename, "r") as f:
        zeilen_anz, spalten_anz, bekannt = f.readline().split()
        zeilen_anz, spalten_anz = int(zeilen_anz), int(spalten_anz)
        for lines in range(zeilen_anz):
            new_line = []
            for element in f.readline().split():
                if element == "y":
                    new_line.append(1)
                elif element == "?":
                    new_line.append(-1)
                else:
                    new_line.append(0)
            matrix.append(new_line)
        known_line = f.readline().split()
        for x in range(len(known_line)):
            if known_line[x] == "y":
                known_line[x] = 1
            elif known_line[x] == "n":
                known_line[x] = 0
            else:
                known_line[x] = -1
        if bekannt == "y":
            bekannt = True
        else:
            bekannt = False
    return matrix, zeilen_anz, spalten_anz, known_line, bekannt

# Quasi inverse Funktion zu create_binary_matrix
def create_columns(matrix):
    columns = []
    for i in range(len(matrix[0])):
        column = []
        for j in range(len(matrix)):
            column.append(matrix[j][i])
        columns.append(column)
    return columns

def zeile_bekannt(matrix, zeile):
    pass

def zeile_unbekannt(matrix, zeile):
    pass


if __name__ == "__main__":

    filenum = input("Enter the number of the file you want to use (00 - 13): ")
    filename = f"auf3/data/konfetti{filenum}.txt"
    matrix, zeilen_anz, spalten_anz, zeile, zeile_gegeben = create_binary_matrix(filename)

    if zeile_gegeben:
        zeile_bekannt(matrix, zeile)
    else:
        zeile_unbekannt(matrix, zeile)