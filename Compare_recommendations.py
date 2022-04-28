import numpy as np
import pandas as pd

hs_nomenclature = "input/HS_2017.csv"

file1 = "input/HS_similarity_usingCF.csv"
file2 = "input/HS92_proximities_fromHarvard.csv"
file3 = "input/HS_proximities_fromSemanticAnalysis.csv"
file4 = "input/HS_proximities_in_HS_nomenclature.csv"

all_files = [file2, file3]

def doRecommendation(hs, file, k=5):
	#return 'k' products near 'hs' according to the adjacency list in 'file'
	result = []

	a = pd.read_csv(file).to_numpy()
	
	#a = [a[i][1] if a[i][0] == "0204" else [] for i in range(0,len(a))]
	b = [str(int(a[i][1])).zfill(4) for i in range(0,len(a)) if (a[i][0] == int(hs)) and (a[i][1] != int(hs))]
	c = [a[i][2] for i in range(0,len(a)) if (a[i][0] == int(hs)) and (a[i][1] != int(hs))]

	result = np.column_stack((b, c))
	result =  sorted(result, key=lambda x:x[1])
	result = [result[i][0] for i in range(0,len(result))]
	result = result[0:k]
	return result


nb_results = 5
nb_hs = 0
total_union = 0
hs_codes = pd.read_csv(hs_nomenclature, dtype="str").to_numpy()
for i in range(0,len(hs_codes)):
	total_reco = []
	empty_recommendation = 0
	for j in range(0, len(all_files)):
		reco = doRecommendation(hs_codes[i], all_files[j], nb_results)
		if (len(reco) == 0):
			empty_recommendation = 1
		total_reco = total_reco + reco
		print(hs_codes[i],"->",reco)
	print(total_reco)
	print(set(total_reco))
	union_cpt = len(total_reco) - len(set(total_reco)) 
	print("taille union=", union_cpt)
	if (empty_recommendation == 0):
		nb_hs = nb_hs + 1
	total_union = total_union + union_cpt

print("File 1: ", all_files[0])
print("File 2: ", all_files[1])
print("Nb recommendations processed: ", nb_hs)
print("Nb max result per recommendation: ", nb_results)
print("Nb duplicates: ", total_union)
print("ppercent duplicates per  prediction: ", float(total_union / nb_hs))
print("percent identical prediction recall@&k: ", float(total_union / nb_hs)/nb_results)

