import numpy as np
import pandas as pd

file1 = "input/HS_similarity_usingCF.csv"
file2 = "input/HS92_proximities_fromHarvard.csv"
file3 = "input/HS_proximities_fromSemanticAnalysis.csv"
file4 = "input/HS_proximities_in_HS_nomenclature.csv"

def doRecommendation(hs, file, k=5):
	#return 'k' products near 'hs' according to the adjacency list in 'file'
	result = []

	#types_dict = {'origin':  str, 'target': str, 'weight': float}
	#a = pd.read_csv(file, header=None).to_numpy(dtype=types_dict)
	a = pd.read_csv(file).to_numpy()
	#a = pd.read_csv(file).to_numpy()
	
	#a = [a[i][1] if a[i][0] == "0204" else [] for i in range(0,len(a))]
	b = [str(int(a[i][1])).zfill(4) for i in range(0,len(a)) if (a[i][0] == int(hs)) and (a[i][1] != int(hs))]
	c = [a[i][2] for i in range(0,len(a)) if (a[i][0] == int(hs)) and (a[i][1] != int(hs))]
	#a = np.array(a, dtype = [('origin', str), ('target', str), ('weight', float)])
	#a = np.array(a, dtype=types_dict)
	#a[ :, a[1].argsort()]


	result = np.column_stack((b, c))
	result =  sorted(result, key=lambda x:x[1])
	result = [result[i][0] for i in range(0,len(result))]
	result = result[0:k]
	return result

reco = doRecommendation("0204", file4, 5)

print(reco)