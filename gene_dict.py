import pandas as pd
import numpy as np

import TreeLib

critical_gene_thresh = 20

def score(dep,method="exp"):
	if method=="exp":
		return np.exp(-dep)

def retrieve_critical_genes():
	trees = TreeLib.load_trees()

	fc=open("data/clusters.tsv")
	idx2clusters={line.split('\t')[0]:line.split('\t')[1].rstrip('\n').split(',') for line in fc}
	clusters2idx={patient:
				  {int(idx2clusters[patient][j]):j for j in range(len(idx2clusters[patient]))}
				  for patient in idx2clusters}

	scores={gene:0. for gene in gene_list}
	for patient,gene in mapping:
		#print mapping[(patient,gene)]
		clusterid,exist=mapping[(patient,gene)]
		if exist!=True  or (patient not in trees): continue;
		node="v%d"%(clusters2idx[patient][clusterid]+1)
		tmp=0.
		for tree in trees[patient]:
			tmp+=score(tree.depth[node],method="exp")
		tmp/=len(trees[patient])
		scores[gene]+=tmp

	sc = pd.DataFrame.from_dict(scores,orient="index")
	return list(sc[sc[0]>critical_gene_thresh].index)



hugo_symbol = pd.read_csv('data/Hugo_Symbol.csv').dropna()
hugo_symbol.PyClonePhyloCluster = hugo_symbol.PyClonePhyloCluster.astype(int)

df = pd.read_csv('data/clusters.tsv', sep='\t', header=None)
df.columns = ['SampleID', 'clusters_kept']
df.clusters_kept = df.clusters_kept.apply(lambda x: set([int(num) for num in x.split(',')]))
clusters_exist = dict(zip(df.SampleID, df.clusters_kept))
hugo_symbol['exist'] = hugo_symbol.apply(lambda x: x.PyClonePhyloCluster in clusters_exist[x.SampleID]
										 if x.SampleID in clusters_exist else None, axis=1)
hugo_symbol = hugo_symbol[hugo_symbol.exist==True].copy()
hugo_symbol['combined_key'] = hugo_symbol.apply(lambda x: (x.SampleID, x.Hugo_Symbol), axis=1)
hugo_symbol['combined_value'] = hugo_symbol.apply(lambda x: (x.PyClonePhyloCluster, x.exist), axis=1)

grouped = hugo_symbol.groupby(['combined_key'])
ind = []
for name, group in grouped:
	ind.append(group.PyClonePhyloCluster.idxmin())
hugo_symbol = hugo_symbol.loc[ind, ].copy()

mapping = dict(zip(hugo_symbol.combined_key, hugo_symbol.combined_value))
gene_list = set(hugo_symbol['Hugo_Symbol'])

mapping_to_gene = {}
critical_genes = retrieve_critical_genes()

hugo_symbol['combined_cluster'] = hugo_symbol.apply(lambda x: (x.SampleID, x.PyClonePhyloCluster), axis=1)
grouped = hugo_symbol.groupby(['combined_cluster'])
for name, group in grouped:
    mapping_to_gene[name] = set(critical_genes).intersection(set(group['Hugo_Symbol']))