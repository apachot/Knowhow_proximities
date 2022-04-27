import numpy as np
import pandas as pd
import codecs

def Compare_section(hs1,hs2):
	I=["01","02","03","04","05"]
	II=["07","08","11"]
	III=["15"]
	IV=["20"]
	V=["25","26","27"]
	VI=["28","29","30","31","32","33","34","35","36","37","38"]
	VII=["39","40"]
	VIII=["41","42","43"]
	IX=["44","45","46"]
	X=["47","48","49"]
	XI=["50","51","52","53","54","55","56","57","58","59","60","61","62","63"]
	XII=["64","65","66","67"]
	XIII=["68","69","70"]
	XIV=["71"]
	XV=["72","73","74","75","76","77","78","79","80","81","82","83"]
	XVI=["84","85"]
	XVII=["86","87","88","89"]
	XVIII=["90","91","92"]
	XIX=["93"]
	XX=["94","95","96"]
	XXI=["97"]

	HS_sections = [I,II,III,IV,V,VI,VII,VIII,IX,X,XI,XII,XIII,XIV,XV,XVI,XVII,XVIII,XIX,XX,XXI]

	for k in range(0,len(HS_sections)):
		if (hs1 in HS_sections[k] and hs2 in HS_sections[k]):
			#print("trouvé : hs1=", hs1, " et " , hs2 , " sont dans la section :", HS_sections[k])
			return True
	return False



#Compare_section("30","37")

file_in = "input/HS_2017.csv"
file_out = "input/HS_proximities_in_HS_nomenclature.csv"

hs = pd.read_csv(file_in, dtype="str").to_numpy()

with codecs.open(file_out, "w", "utf8") as o:
	for i in range (0, len(hs)):
		for j in range(0, len(hs)):
			weight = 1
			if (Compare_section(hs[i][0][0:2],hs[j][0][0:2])):
				weight = .75
			if (hs[i][0][0:3] == hs[j][0][0:3]):
				weight = .25
			if (hs[i][0][0:4] == hs[j][0][0:4]):
				weight = 0

			if (weight != 1):
				print(hs[i][0],",",hs[j][0],",",weight)
				o.write(f"{hs[i][0]},{hs[j][0]},{weight}\n")




 
            