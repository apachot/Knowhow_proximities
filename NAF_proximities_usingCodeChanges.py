import pandas as pd
import numpy as np
from sklearn.manifold import MDS
from matplotlib import pyplot as plt
from scipy.stats import wasserstein_distance

from sklearn.metrics.pairwise import cosine_similarity

def group_weighted_mean_factory(df: pd.DataFrame, weight_col_name: str):
    # Ref: https://stackoverflow.com/a/69787938/
    def group_weighted_mean(x):
        try:
            return np.average(x, weights=df.loc[x.index, weight_col_name])
        except ZeroDivisionError:
            return np.average(x)
    return group_weighted_mean

#nomenclature_HS2017 = pd.read_csv('./data/HS2017_4digits.csv', delimiter=',', header=0).to_numpy()
nomenclature_NAF = pd.read_csv('./input/NAF_2.csv', delimiter=',', header=0).to_numpy()
productive_jumps = pd.read_csv('./input/NAF_proximities_usingCodeChanges.csv', delimiter=',', header=0, dtype={'proximity': float}).to_numpy()

# Import HS2017 nomenclature as HS_2017
nomenclature_HS2017 = pd.read_csv('./input/HS_2017.csv', delimiter=',', header=0).to_numpy()
# Impoort HS2017 to NACE2 crosswalk as correspondance_HS2017_NACE2
correspondance_HS2017_NAF2 = pd.read_csv('./input/NAF_HS4.csv', delimiter=',', header=1).to_numpy()


nomenclature_NAF = nomenclature_NAF[:,0]
#print(nomenclature_NAF)


len_NAF = len(np.unique(nomenclature_NAF))



#print("unique=", len(np.array(productive_jumps[0]).unique()))
#building a dissimilarity matrix from harvard proximities
dissimilarity_matrix = np.ones((len_NAF,len_NAF))
for i in range(0, len(productive_jumps)):
	NAF_code1 = productive_jumps[i,0]
	NAF_code2 = productive_jumps[i,1]
	NAF_proximity = productive_jumps[i,2]
	
	#print("NAF_code1", NAF_code1, "NAF_code2", NAF_code2)
	
	#looking for the index of each hs 2017 code in the nomenclature
	idx_NAF_code1_nomenclature =  np.where(nomenclature_NAF==NAF_code1)
	idx_NAF_code2_nomenclature =  np.where(nomenclature_NAF==NAF_code2)

	#print("idx_NAF_code1_nomenclature", idx_NAF_code1_nomenclature)
	#print("idx_NAF_code2_nomenclature", idx_NAF_code2_nomenclature)

	dissimilarity_matrix[idx_NAF_code1_nomenclature[0], idx_NAF_code1_nomenclature[0]] = 0
	dissimilarity_matrix[idx_NAF_code2_nomenclature[0], idx_NAF_code2_nomenclature[0]] = 0
	dissimilarity_matrix[idx_NAF_code1_nomenclature[0], idx_NAF_code2_nomenclature[0]] = NAF_proximity
	dissimilarity_matrix[idx_NAF_code2_nomenclature[0], idx_NAF_code1_nomenclature[0]] = NAF_proximity


print(dissimilarity_matrix)
var_dimension = 100
embedding = MDS(n_components=var_dimension, verbose=1, dissimilarity='precomputed', max_iter=1000)
dissimilarity_matrix_transformed = embedding.fit_transform(1-dissimilarity_matrix)
print(dissimilarity_matrix_transformed.shape)
print(dissimilarity_matrix_transformed[:1])

pd.DataFrame(dissimilarity_matrix_transformed).to_csv("./output/activity_vector_space_dim_"+str(var_dimension)+".csv")

#looking for similarities between products
products_proximities = cosine_similarity(dissimilarity_matrix_transformed)
print (products_proximities.shape)
print(products_proximities[:3])
pd.DataFrame(products_proximities+1).to_csv("./output/activity_proximities.csv")
"""
for i in range(0, len(nomenclature_HS2017)):
	hs_code = nomenclature_HS2017[i][0]
	print ("HS_CODE=", hs_code)
	#print(correspondance_HS2017_NAF2)
	idx = np.where(correspondance_HS2017_NAF2[:,1]==hs_code)
	print(idx)
	print("taille idx", len(idx[0]))
	for j in range(0, len(idx[0])):
		print('activité trouvée : ', correspondance_HS2017_NAF2[:,0][idx[0][j]] , "poids=", correspondance_HS2017_NAF2[:,2][idx[0][j]])
		vector = 
"""

#products_proximities = cosine_similarity(activity_vector_space)

#building vectors for HS products
#activities_proximities= construct_activities_proximities(nomenclature_NACE2,correspondance_HS2017_NACE2,nomenclature_HS2017,dissimilarity_matrix_transformed)
#def construct_activities_proximities(NACE2,correspondance_HS2017_NACE2,HS2017,activity_vector_space):

"""
concatenate_data = nomenclature_HS2017.merge(correspondance_HS2017_NAF2, left_on=nomenclature_HS2017[0], right_on= correspondance_HS2017_NAF2["HS4"])

# Drop unused column
concatenate_data.drop(columns=["key_0","Label","Id"],inplace=True)
# Insert HS2017 nomebnclature in activity_vector_space
prod_vec_space =pd.DataFrame(activity_vector_space, index=correspondance_HS2017_NAF2["HS4"].sort_values().unique())    # Merge activity_vector_space with HS2017 to NACE2 crosswalk
product_vector_final = concatenate_data.merge(prod_vec_space, left_on=concatenate_data["HS4"], right_on=prod_vec_space.index)

# Drop redundant columns
product_vector_final.drop(columns=["key_0"], inplace=True)

# Compute average proximity between NACE using HS proximities weighted by their contributions in each NACE sectors
group_weighted_mean = group_weighted_mean_factory(product_vector_final, "weight")
activities_prox =  product_vector_final.groupby(["NAF"]).agg(group_weighted_mean)  # Define

# Compute average activities proximities by cosine similarity method
activities_proximities = pd.DataFrame(data = (cosine_similarity(activities_prox.iloc[:,2:])+1)/2, index=activities_prox.index.values, columns=activities_prox.index.values )
"""


