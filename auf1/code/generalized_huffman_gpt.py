import heapq

class _Node:
    __slots__ = ("weight","symbol","children")
    def __init__(self, weight, symbol=None):
        self.weight   = weight      # total leaf‐weight under this node
        self.symbol   = symbol      # leaf: an index; internal: None
        self.children = []          # up to n children, in code‐digit order
    def __lt__(self, other):
        return self.weight < other.weight

def get_data(filename):
    with open(filename, "r") as f:
        n = int(f.readline())
        weight_function = list(map(int, f.readline().split()))
        
        frequency_dict = {}
        text = f.read()
        for char in text:
            if char != "\n":
                if char in frequency_dict:
                    frequency_dict[char] += 1
                else:
                    frequency_dict[char] = 1
    return n, weight_function, frequency_dict, len(text.strip("\n"))

def nary_huffman_with_letter_costs(weights, letter_costs):
    """
    weights:         list of positive ints, w[i] is the weight of symbol i
    letter_costs:    list of n costs, c[0..n-1], one per code‐symbol/branch
    Returns dict { symbol_index -> codeword string }.
    """
    n = len(letter_costs)
    heap = [ _Node(w, symbol=i) for i, w in enumerate(weights) ]
    heapq.heapify(heap)

    # Pad with zero‐weight dummies if needed (only when n>1)
    if n > 1:
        pad = (n-1 - (len(heap)-1)%(n-1)) % (n-1)
        for _ in range(pad):
            heapq.heappush(heap, _Node(0))

    # Precompute branch positions in increasing-cost order
    # (i.e. cheapest‐letter first)
    branch_positions = list(range(n))
    branch_positions.sort(key=lambda i: letter_costs[i])

    # Build the tree
    while len(heap) > 1:
        # 1) take the n lightest nodes
        children = [ heapq.heappop(heap) for _ in range(n) ]

        # 2) sort them heavy→light so we can give the heaviest the cheapest branch
        children.sort(key=lambda node: node.weight, reverse=True)

        # 3) create an array of length n, placing each child in its branch‐slot
        arranged = [None]*n
        for child, slot in zip(children, branch_positions):
            arranged[slot] = child

        # 4) new parent has weight = sum of child weights
        parent = _Node(sum(ch.weight for ch in children))
        parent.children = arranged
        heapq.heappush(heap, parent)

    # Now extract codes by traversing from the single root
    root = heap[0]
    codes = {}
    def _assign(node, prefix):
        if node.symbol is not None:
            # leaf: record code (or "0" if it's the only symbol)
            codes[node.symbol] = prefix or "0"
        else:
            for digit, child in enumerate(node.children):
                _assign(child, prefix + str(digit))
    _assign(root, "")
    return codes


path = "auf1/data/"
input_files = input("Welche Dateien sollen bearbeitet werden?").split()
for x in input_files:
    file = f"schmuck{x}.txt"
    n, costs, freq, text_len = get_data(path+file)

    codes = nary_huffman_with_letter_costs(list(freq.values()), costs)
    for i, code in sorted(codes.items()):
        print(f"symbol {i} (w={list(freq.values())[i]}) → {code}")
