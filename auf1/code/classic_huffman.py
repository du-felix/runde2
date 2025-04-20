import heapq

class Node:
    def __init__(self, symbol, frequency, children=None):
        self.symbol = symbol
        self.frequency = frequency
        self.children = children if children is not None else []
        self.code = ""

    def set_freq(self):
        freq = 0
        for child in self.children:
            freq += child.frequency
        self.frequency = freq

    def __lt__(self, other):
        # For priority queue comparison based on frequency
        return self.frequency < other.frequency

def get_data(filename):
    with open(filename, "r") as f:
        n = int(f.readline())
        weight_function = map(int, f.readline().split())
        frequency_dict = {}
        text = f.read()
        for char in text:
            if char != "\n":
                if char in frequency_dict:
                    frequency_dict[char] += 1
                else:
                    frequency_dict[char] = 1
    return n, weight_function, frequency_dict

def build_huffman(n, frequencies):
    pq = []
    for symbol, freq in frequencies.items():
        heapq.heappush(pq, Node(symbol, freq))

    remainder = (len(pq)-1) % (n-1)
    if remainder != 0:
        dummy_num = n - 1 - remainder
        for _ in range(dummy_num):
            heapq.heappush(pq, Node(None, 0))    

    while len(pq) > 1:
        children = [heapq.heappop(pq) for _ in range(min(n, len(pq)))]
        internal_node = Node(None, None, children=children)
        internal_node.set_freq()
        heapq.heappush(pq, internal_node)
    
    return pq[0]

def assign_codes(node, code, n):
    node.code = code
    for i, child in enumerate(node.children):
        if child.symbol is not None or child.children:
            assign_codes(child, code + str(i), n)

def get_codes(root):
    codes = {}

    def traverse(node):
        if node.symbol is not None:
            codes[node.symbol] = node.code
        for child in node.children:
            traverse(child)

    traverse(root)
    return codes

if __name__ == "__main__":
    path = "auf1/data/"
    input_files = input("Welche Dateien sollen bearbeitet werden?").split()
    for x in input_files:
        file = f"schmuck{x}.txt"
        n, _, freq = get_data(path+file)
        root = build_huffman(n, freq)
        assign_codes(root, "", n)
        codes = get_codes(root)
        for symbol, code in codes.items():
            print(f"{symbol}: {code}")
        total_length = 0
        for symbol, f in freq.items():
            cost = len(codes[symbol])
            total_length += cost*f
        print(total_length)