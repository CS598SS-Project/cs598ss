import pandas as pd
import numpy as np

import DistanceLib
import TreeLib

trees=TreeLib.load_trees()

def init_trees(n):
	df = pd.DataFrame(np.zeros((len(trees), 3)))
	df.columns = ['good_tree', 'cluster', 'patient']
	df.patient = trees.keys()
	df.good_tree = df.apply(lambda x: np.random.randint(len(trees[x.patient])), axis=1)
	df.cluster = df.cluster.apply(lambda x: np.random.randint(n))
	return df

def recenter(n, chosen_trees):
	centers =[]
	for k in range(n):
		cluster_k_rows = chosen_trees[chosen_trees.cluster==k].copy()
		# cluster_k_trees = cluster_k_rows.apply(lambda x: trees[x.patient][x.good_tree], axis=1)
		cluster_k_trees = [trees[row.patient][row.good_tree] for index, row in cluster_k_rows.iterrows()]
		centers.append(DistanceLib.cal_w(cluster_k_trees))
	return centers

def reassign(chosen_tree_row, centers):
	patient_trees = trees[chosen_tree_row.patient]
	dist = 1e300
	chosen_tree_row.good_tree = -1
	chosen_tree_row.cluster = -1
	for t in range(len(patient_trees)):
		for c in range(len(centers)):
			dist_now = DistanceLib.distance_profile(patient_trees[t], centers[c])
			if dist_now < dist:
				chosen_tree_row.good_tree = t
				chosen_tree_row.cluster = c
				dist = dist_now
	return chosen_tree_row	
	
def tree_kmeans(n):
	# chosen_trees[i, 'good_tree'] = j => tree j is representative of patient i
	# chosen_trees[i, 'cluster'] = k => patient i is assigned to cluster k
	# chosen_trees[i, 'patient'] = i => for convenience
	chosen_trees = init_trees(n) # random initialization?
	converged = False
	agreed_thresh = 5
	max_iter = 20
	for current_iter in range(max_iter):
		# centers[0] = consensus tree for cluster 0
		centers = recenter(n, chosen_trees)
		old_choice = chosen_trees.good_tree
		# update (representative tree, corresponding cluster) pair
		# display(chosen_trees)
		print(chosen_trees.cluster.value_counts())
		chosen_trees = chosen_trees.apply(lambda x: reassign(x, centers), axis=1)
		# break the loop if the representative trees converge
		disagreement = sum(old_choice!=chosen_trees.good_tree)
		print('iter %d, disagreement %d' % (current_iter, disagreement))
		# print(old_choice[:3])
		if disagreement < agreed_thresh:
			converged = True
			break
	return chosen_trees, centers, converged