from flask import Flask, render_template, request
import time

app = Flask(__name__)


class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.rank = [0] * (n + 1)
        self.operations = 0

    def find(self, x):
        self.operations += 1
        if self.parent[x] != x:
            self.operations += 1
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)
        self.operations += 2

        if root_a == root_b:
            return False

        if self.rank[root_a] < self.rank[root_b]:
            self.parent[root_a] = root_b
        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a
        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1

        self.operations += 2
        return True


def parse_edges(raw_text, office_count):
    if not raw_text or not raw_text.strip():
        raise ValueError("Please provide at least one link in the format: office1 office2 cost [bandwidth].")

    edges = []
    lines = raw_text.strip().splitlines()

    for index, line in enumerate(lines, start=1):
        parts = line.replace(",", " ").split()
        if len(parts) < 3:
            raise ValueError(f"Line {index} is invalid. Use: office1 office2 cost [bandwidth].")

        try:
            u = int(parts[0])
            v = int(parts[1])
            cost = float(parts[2])
        except ValueError as exc:
            raise ValueError(f"Line {index} has invalid numeric values.") from exc

        if not (1 <= u <= office_count and 1 <= v <= office_count):
            raise ValueError(f"Line {index} uses an office number outside the valid range 1 to {office_count}.")

        if u == v:
            raise ValueError(f"Line {index} is invalid because an office cannot connect to itself.")

        bandwidth = int(parts[3]) if len(parts) >= 4 else None
        edges.append((u, v, cost, bandwidth))

    return edges


def prim_mst(office_count, edges):
    adjacency = {i: [] for i in range(1, office_count + 1)}
    for u, v, cost, bandwidth in edges:
        adjacency[u].append((v, cost, bandwidth))
        adjacency[v].append((u, cost, bandwidth))

    selected = [False] * (office_count + 1)
    key = [float("inf")] * (office_count + 1)
    parent = [None] * (office_count + 1)
    key[1] = 0.0
    operations = 0
    mst_edges = []

    for _ in range(office_count):
        min_vertex = None
        min_value = float("inf")

        for vertex in range(1, office_count + 1):
            operations += 1
            if not selected[vertex] and key[vertex] < min_value:
                min_value = key[vertex]
                min_vertex = vertex

        if min_vertex is None:
            break

        selected[min_vertex] = True
        operations += 1

        if parent[min_vertex] is not None:
            mst_edges.append((parent[min_vertex], min_vertex, key[min_vertex]))

        for neighbor, weight, _ in adjacency[min_vertex]:
            operations += 1
            if not selected[neighbor] and weight < key[neighbor]:
                key[neighbor] = weight
                parent[neighbor] = min_vertex
                operations += 2

    total_cost = sum(edge[2] for edge in mst_edges)
    return mst_edges, total_cost, operations


def kruskal_mst(office_count, edges):
    sorted_edges = sorted(edges, key=lambda item: item[2])
    dsu = DisjointSet(office_count)
    mst_edges = []
    total_cost = 0.0
    operations = 0

    for u, v, cost, bandwidth in sorted_edges:
        operations += 1
        if dsu.union(u, v):
            mst_edges.append((u, v, cost))
            total_cost += cost
            operations += 1

    operations += dsu.operations
    return mst_edges, total_cost, operations


def compare_algorithms(office_count, edges):
    start_prim = time.perf_counter()
    prim_edges, prim_total, prim_ops = prim_mst(office_count, edges)
    end_prim = time.perf_counter()

    start_kruskal = time.perf_counter()
    kruskal_edges, kruskal_total, kruskal_ops = kruskal_mst(office_count, edges)
    end_kruskal = time.perf_counter()

    return {
        "vertices": office_count,
        "edges": len(edges),
        "prim_edges": prim_edges,
        "kruskal_edges": kruskal_edges,
        "prim_total": prim_total,
        "kruskal_total": kruskal_total,
        "prim_time_ms": round((end_prim - start_prim) * 1000, 6),
        "kruskal_time_ms": round((end_kruskal - start_kruskal) * 1000, 6),
        "prim_operations": prim_ops,
        "kruskal_operations": kruskal_ops,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        try:
            office_count = int(request.form.get("offices", 0))
            raw_edges = request.form.get("edges", "")

            if office_count <= 0:
                raise ValueError("The number of offices must be greater than zero.")

            edges = parse_edges(raw_edges, office_count)
            result = compare_algorithms(office_count, edges)
        except ValueError as exc:
            error = str(exc)

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


