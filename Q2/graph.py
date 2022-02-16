class Graph:
    def __init__(self, V = {}, E = {}):
        self.E = set(frozenset((u, v)) for u, v in E)
        self._nbrs = {}
        for v in V:
            self.add_vertex(v)
        for u, v in self.E:
            self.add_edge(u, v)

    def add_vertex(self, v):
        if v not in self._nbrs:
            self._nbrs[v] = set()

    def remove_vertex(self, u):
        to_delete = list(self.nbrs(u))
        for v in to_delete:
            self.remove_edge(u, v)
        del self._nbrs[u]

    def add_edge(self, u, v):
        self.add_vertex(u)
        self.add_vertex(v)
        self.E.add(frozenset([u, v]))
        self._nbrs[u].add(v)
        self._nbrs[v].add(u)

    def remove_edge(self, u, v):
        e = frozenset([u, v])
        if e in self.E:
            self.E.remove(e)
            self._nbrs[u].remove(v)
            self._nbrs[v].remove(u)

    def deg(self, v):
        return len(self._nbrs[v])

    def nbrs(self, v):
        return iter(self._nbrs[v])

    def vertices(self):
        V = set()
        for v in self._nbrs:
            V.add(v)
        return V

    @property
    def m(self):
        return len(self.E)

    @property
    def n(self):
        return len(self._nbrs)


if __name__ == '__main__':
    G = Graph([1, 2, 3], {(1, 2), (2, 3)})
    assert(G.deg(1) == 1)
    assert(G.deg(2) == 2)
    assert(G.deg(3) == 1)
    assert(set(G.nbrs(2)) == {1, 3})
    assert(G.n == 3 and G.m == 2)
    
    G.remove_edge(1, 2)
    assert(G.n == 3 and G.m == 1)
    
    G.remove_edge(1, 3)
    assert(G.n == 3 and G.m == 1)

    G.add_edge(1, 2)
    assert(G.n == 3 and G.m == 2)

    G.remove_vertex(2)
    assert(G.n == 2 and G.m == 0)
    
    print("Okay")
