import pandas as pd

def load_dict():
	hugo_symbol = pd.read_csv('data/Hugo_Symbol.csv').dropna()
	hugo_symbol.PyClonePhyloCluster = hugo_symbol.PyClonePhyloCluster.astype(int)
	hugo_symbol['combined'] = hugo_symbol.apply(lambda x: (x.SampleID, x.Hugo_Symbol), axis=1)
	mapping = dict(zip(hugo_symbol.combined, hugo_symbol['PyClonePhyloCluster']))
	gene_list = set(hugo_symbol['Hugo_Symbol'])
	return mapping, gene_list