# import des fonctions
from UserAssistFunctions import *

# On récupère et parcourt les liens des sous clés
hivesPathList = getHivesPathList()
for hivePath in hivesPathList :
    
    # On récupère et parcourt les lignes de la sous clé si elle en a
    hiveLines = getHiveLines(hivePath)
    if(len(hiveLines) != 0) :
        for line in hiveLines :
            
            # On affiche la ligne
            print(hivePath)