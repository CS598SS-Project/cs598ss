import gene_dict

fc=open("data/clusters.tsv")
idx2clusters={line.split('\t')[0]:line.split('\t')[1].rstrip('\n').split(',') for line in fc}
mapping,genes=gene_dict.load_dict()
clusters2idx={patient:
              {int(idx2clusters[patient][j]):j for j in range(len(idx2clusters[patient]))}
              for patient in idx2clusters}
critical_gene=gene_dict.retrieve_critical_genes()

def relation(t,g1,g2):
    if ((t.patient,g1) not in mapping) or ((t.patient,g2) not in mapping) :
        return "no_relation";
    id1,_=mapping[(t.patient,g1)]
    id2,_=mapping[(t.patient,g2)]
    node1="v%d"%(clusters2idx[t.patient][id1]+1)
    node2="v%d"%(clusters2idx[t.patient][id2]+1)
    if t.parent[node1]==node2:
        return "child"
    if t.parent[node2]==node1:
        return "parent"
    if node1==node2:
        return "self"
    return "no_relation"

def distance(t1,t2):
    answer=0.
    for i in range(len(critical_gene)):
        for j in range(i):
            g1,g2=critical_gene[i],critical_gene[j]
            r1=relation(t1,g1,g2)
            r2=relation(t2,g1,g2)
            if r1==r2: 
                continue
            if r1=="no_relation" or  r2=="no_relation":
                answer+=1
                continue
            if r1=="self" or r2=="self":
                answer+=1
                continue
            answer+=2
    return answer

def cal_w(trees):
    # import pdb; pdb.set_trace()
    w={f:{g:0. for g in critical_gene} for f in critical_gene}
    for i in range(len(critical_gene)):
        for j in range(i):
            g1,g2=critical_gene[i],critical_gene[j]
            for t in trees:
                r=relation(t,g1,g2)
                if r=="child":
                    w[g2][g1]+=1
                if r=="parent":
                    w[g1][g2]+=1
                if r=="self":
                    w[g1][g2]+=0.5
                    w[g2][g1]+=0.5
            w[g1][g2]/=len(trees)
            w[g2][g1]/=len(trees)
    return w

def distance_profile(t,w):
    answer=0.
    for i in range(len(critical_gene)):
        for j in range(i):
            g1,g2=critical_gene[i],critical_gene[j]
            r=relation(t,g1,g2)
            if r=="child":
                answer+= 1-w[g2][g1]
                answer+= w[g1][g2]
            if r=="parent":
                answer+= 1-w[g1][g2]
                answer+=w[g2][g1]
            if r=="self":
                answer+=abs(.5-w[g1][g2])
                answer+=abs(.5-w[g2][g1])
            if r=="no_relation":
                answer+= w[g1][g2]
                answer+= w[g2][g1]
    return answer
