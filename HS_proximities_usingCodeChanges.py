import numpy as np
import pandas as pd
import csv
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse
import codecs

var_dimension = 100

nomenclature_HS2017 = pd.read_csv('./input/HS_2017.csv', delimiter=',', header=0).to_numpy()
correspondance_HS2017_NAF = pd.read_csv('./input/NAF_HS4.csv', delimiter=',', header=0).to_numpy()
#nomenclature_NAF = pd.read_csv('./data/NACE_2.csv', delimiter=',', header=None).to_numpy()
nomenclature_NAF = pd.read_csv('./input/NAF_2.csv', delimiter=',', header=0).to_numpy()
activity_vector_space = pd.read_csv('./output/activity_vector_space_dim_'+str(var_dimension)+'.csv', delimiter=',', header=0, index_col=0).to_numpy()

print (activity_vector_space.shape)
print(activity_vector_space[:3])


print (nomenclature_HS2017.shape)
print(nomenclature_HS2017[:3])

tab_products_vectors = np.zeros((len(nomenclature_HS2017), var_dimension))
#tab_real_NACE = []

for i in range(0, len(nomenclature_HS2017)):
	HS_code = nomenclature_HS2017[i,0]
	print('code = ', HS_code)
	idx_HS_code =  np.where(correspondance_HS2017_NAF[:,1]==HS_code)
	nb_HS_code = len(idx_HS_code[0])
	if (nb_HS_code > 0):
		tab_NAF_vectors = np.zeros((nb_HS_code, var_dimension))
		tab_NAF_weights = np.zeros(nb_HS_code)
		print("trouvé, len=",nb_HS_code)
		for j in range(0, nb_HS_code):
			NAF_code = correspondance_HS2017_NAF[idx_HS_code[0],0][j]
			NAF_weight = correspondance_HS2017_NAF[idx_HS_code[0],2][j]
			tab_NAF_weights[j] = NAF_weight
			print("NAF_code=",NAF_code,"NAF_weight=",NAF_weight)
			#looking for the index of the HS code in the nomenclature
			idx_NAF_code =  np.where(nomenclature_NAF[:,0]==NAF_code)
			if (len(idx_NAF_code[0]) > 0):
				#we load the product vector
				NAF_vector = activity_vector_space[idx_NAF_code[0],:][0]
				print("NAF-vector=",NAF_vector)
				print(NAF_vector.shape)
				print(tab_NAF_vectors.shape)
				tab_NAF_vectors[j] = NAF_vector
			else:
				print('error, NAF code not found in the nomenclature')

		print("tab_NAF_vectors=", tab_NAF_vectors)
		#we do a weighted average of vectors

		average_NAF_vector = np.average(tab_NAF_vectors, axis=0, weights=tab_NAF_weights)

		print("i=", i, "len(nomenclature_HS2017)", len(nomenclature_HS2017))
		print("average_NAF_vector=", average_NAF_vector)
		tab_products_vectors[i] = average_NAF_vector



	else:
		print("not found")

print ("tab_products_vectors=", tab_products_vectors)
print(tab_products_vectors.shape)

pd.DataFrame(tab_products_vectors).to_csv("./output/tab_products_vectors.csv")

#looking for similarities between activities
products_proximities = cosine_similarity(tab_products_vectors)
print (products_proximities.shape)
print(products_proximities[:3])
#pd.DataFrame((products_proximities+1)/2).to_csv("./output/HS_proximities_usingMDSandNAFchanges.csv")


a = np.array([['source','target','weight']])
file_out = "./output/HS_proximities_usingMDSandNAFchanges.csv"
with codecs.open(file_out, "w", "utf8") as o:
	for i in range(0, len(products_proximities)):
		for j in range(0, len(products_proximities[i])):
			if((products_proximities[i][j]) >= 0 and (products_proximities[i][j] > .6)):
				b = np.array([[nomenclature_HS2017[i][0],nomenclature_HS2017[j][0],np.round(1-products_proximities[i][j],4)]])
				a = np.concatenate((a, b), axis=1)
				print (str(nomenclature_HS2017[i][0]).zfill(4),str(nomenclature_HS2017[j][0]).zfill(4),np.round(1-products_proximities[i][j],4))
				o.write(f"{str(nomenclature_HS2017[i][0]).zfill(4)},{str(nomenclature_HS2017[j][0]).zfill(4)},{np.round(1-products_proximities[i][j],4)}\n")


#pd.DataFrame(products_proximities).to_csv("./output/HS_proximities_usingMDSandNAFchanges.csv")

				
