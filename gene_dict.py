import pandas as pd

hugo_symbol = pd.read_csv('data/Hugo_Symbol.csv').dropna()
hugo_symbol.PyClonePhyloCluster = hugo_symbol.PyClonePhyloCluster.astype(int)
hugo_symbol['combined'] = hugo_symbol.apply(lambda x: (x.SampleID, x.Hugo_Symbol), axis=1)
mapping = dict(zip(hugo_symbol.combined, hugo_symbol['PyClonePhyloCluster']))