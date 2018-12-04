class Tree:
    def __init__(self):
        self.node=[]
        self.depth={}
        self.edge=[]
        self.parent={}
        self.child={}
        self.root=None
    
    def add_edge(self,v1,v2):
        #an arc from v1 to v2
        if v1 not in self.node:
            self.node.append(v1)
        if v2 not in self.node:
            self.node.append(v2)
        self.edge.append((v1,v2))
    
    def construct_tree(self):
        for v in self.node:
            self.child[v]=[]
            self.parent[v]=None
        for (v1,v2) in self.edge:
            self.parent[v2]=v1
            self.child[v1].append(v2)
    
    def find_root(self):
        v=self.node[0]
        while self.parent[v]!=None:
            v=self.parent[v]
        self.root=v
    
    def find_depth(self, node, dep=0):
        self.depth[node]=dep;
        for child in self.child[node]:
            self.find_depth(child,dep+1)
