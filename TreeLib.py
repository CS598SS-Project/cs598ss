import glob
import numpy as np

max_trees = 20

class Tree:
    def __init__(self,patient):
        self.patient=patient
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

def readtrees(patient):
    tree_file = open("data/input/T_%s.txt"%patient,"r")
    N_clusters=tree_file.readline().split()[1]
    N_clusters=int(N_clusters)
    N_trees=tree_file.readline().split()[0]
    N_trees=int(N_trees)
    trees=[]
    for i in range(N_trees):
        tree=Tree(patient)
        for j in range(N_clusters):
            line=tree_file.readline()
            if j==0: continue
            v1,v2=line.rstrip("\n").split()
            tree.add_edge(v1,v2)
        tree.construct_tree()
        tree.find_root()
        tree.find_depth(tree.root)
        trees.append(tree)
    return trees        

def load_trees():
    patients=[]
    trees_patient={}
    for filename in glob.glob("data/input/T_*.txt"):
        patient=filename.lstrip("data/input/T_").rstrip(".txt")
        trees=readtrees(patient)
        if(len(trees)==0):continue
        patients.append(patient)
        trees_patient[patient]=trees
        
    trees={p:trees_patient[p] for p in trees_patient if len(trees_patient[p])>0 }
    for patient in trees:
        len_now = len(trees[patient])
        if len_now>max_trees:
            arr = np.arange(len_now)
            np.random.shuffle(arr)
            indices = arr[:max_trees]
            trees[patient] = [trees[patient][i] for i in indices]
    return trees