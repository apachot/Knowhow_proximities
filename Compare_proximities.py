import pandas as pd
import networkx as nx
import netcomp as nc

file1 = "input/HS_similarity_usingCF.csv"
file2 = "input/HS92_proximities_fromHarvard.csv"
file3 = "input/HS_proximities_fromSemanticAnalysis.csv"
file4 = "input/HS_proximities_in_HS_nomenclature.csv"

tables_list = [file1,file2,file3,file4]

for i in range(0, len(tables_list)):
	for j in range (0, len(tables_list)):

		#=============
		fileA = tables_list[i]
		fileB = tables_list[j]
		#=============

		print("Comparing :")

		print("- ", fileA)
		print("- ", fileB)

		G_A = nx.read_weighted_edgelist(fileA, delimiter=",")
		G_B = nx.read_weighted_edgelist(fileB, delimiter=",")

		A,B = [nx.adjacency_matrix(G) for G in [G_A,G_B]]

		print("matrix distances :")
		r4 = nc.deltacon0(A,B);
		print("deltacon0", r4)
		r5 = nc.vertex_edge_distance(A,B);
		print("vertex_edge_distance", r5)

		print("spectral distances :")
		r7 = nc.lambda_dist(A,B);
		print("lambda_dist", r7)
		r1 = nc.lambda_dist(A,B,kind='laplacian',k=10)
		print("lambda_dist(laplacian)",r1)
		r8 = nc.lambda_dist(A,B,kind='adjacency',k=2);
		print("lambda_dist(adjacency,k=2)", r8)
		r9 = nc.lambda_dist(A,B,kind='laplacian_norm');
		print("lambda_dist(laplacian_norm,k=2)", r9)

		print("other distances")
		r10 = nc.resistance_distance(A,B,renormalized=True);
		print("resistance_distance", r10)
