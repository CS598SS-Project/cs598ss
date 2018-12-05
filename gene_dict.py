import pandas as pd

def load_dict():
	hugo_symbol = pd.read_csv('data/Hugo_Symbol.csv').dropna()
	hugo_symbol.PyClonePhyloCluster = hugo_symbol.PyClonePhyloCluster.astype(int)
	
	df = pd.read_csv('data/clusters.tsv', sep='\t', header=None)
	df.columns = ['SampleID', 'clusters_kept']
	df.clusters_kept = df.clusters_kept.apply(lambda x: set([int(num) for num in x.split(',')]))
	clusters_exist = dict(zip(df.SampleID, df.clusters_kept))
	hugo_symbol['exist'] = hugo_symbol.apply(lambda x: x.PyClonePhyloCluster in clusters_exist[x.SampleID]
	                                         if x.SampleID in clusters_exist else None, axis=1)
	
	hugo_symbol['combined_key'] = hugo_symbol.apply(lambda x: (x.SampleID, x.Hugo_Symbol), axis=1)
	hugo_symbol['combined_value'] = hugo_symbol.apply(lambda x: (x.PyClonePhyloCluster, x.exist), axis=1)
	
	mapping = dict(zip(hugo_symbol.combined_key, hugo_symbol.combined_value))
	return mapping, gene_list