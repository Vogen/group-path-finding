
class Node:
    def __init__(self, x, y, v=None):
        self.x = x
        self.y = y
        self.v = v
        self.edges = []
    
    def distance(self, t):
        return pow(self.x - t.x, 2) + pow(self.y - t.y, 2)

    def add_edge(self, e):
        self.edges.append(e)

class Edge:
    def __init__(self, s, t):
        self.s = s
        self.t = t
        self.v = s.distance(t)
        self.available = True

class Solver():
    def __init__(self):
        self.match = {}  # point : edge
        self.vis = {}

    def greedy(self, s):
        for e in s.edges:
            if not e.t in self.match:
                self.match[e.t] = e
                return

    def find(self, s):
        # print(s.x, s.y)
        for e in reversed(s.edges):
            if e.available and not self.vis[e.t]:
                self.vis[e.t] = True
                if not e.t in self.match or self.find(self.match[e.t].s):
                    # print(e.s.x, e.s.y, '-', e.t.x, e.t.y)
                    self.match[e.t] = e
                    return True
        return False

    def solve(self, start_points, target_points):
        # create graph
        s_nodes = []
        t_nodes = []
        for p in start_points: s_nodes.append(Node(*p))
        for p in target_points: t_nodes.append(Node(*p))
        for s in s_nodes:
            for t in t_nodes: s.add_edge(Edge(s, t))
            s.edges.sort(key=lambda x:x.v)

        # baseline
        for s in s_nodes: self.greedy(s)
        cost = max(e.v for t, e in self.match.items())

        # extend
        for _ in range(0):
            res = self.match.copy()

            for s in s_nodes: 
                for e in s.edges:
                    if e.v >= cost:
                        e.available = False
            
            pending_start = []
            for t in t_nodes:
                if self.match[t].v == cost: 
                    e = self.match[t]
                    self.match.pop(t)
                    pending_start.append(e.s)

            self.vis = {}
            for t in t_nodes: self.vis[t] = False

            for s in pending_start: 
                if not self.find(s):
                    return res, cost
                    
            cost = max(e.v for t, e in self.match.items())

        return self.match, cost