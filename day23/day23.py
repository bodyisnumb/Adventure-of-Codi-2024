def parse_input(filename):
    edges = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                a, b = line.split('-')
                edges.append((a, b))
    return edges

def build_graph(edges):
    graph = {}
    for a, b in edges:
        if a not in graph:
            graph[a] = set()
        if b not in graph:
            graph[b] = set()
        graph[a].add(b)
        graph[b].add(a)
    return graph

def find_triangles(graph):
    nodes = sorted(graph.keys())
    triangles = []
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            for k in range(j+1, len(nodes)):
                a, b, c = nodes[i], nodes[j], nodes[k]
                if b in graph[a] and c in graph[a] and c in graph[b]:
                    triangles.append((a,b,c))
    return triangles

def part1(filename):
    edges = parse_input(filename)
    graph = build_graph(edges)
    triangles = find_triangles(graph)
    count = 0
    for tri in triangles:
        if any(x.startswith('t') for x in tri):
            count += 1
    return count

def part2(filename):
    return None

if __name__ == "__main__":
    print(part1("data.txt"))