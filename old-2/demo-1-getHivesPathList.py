# import des fonctions
from UserAssistFunctions import *

# On récupère et parcourt les liens des sous clés
hivesPathList = getHivesPathList()
for hivePath in hivesPathList :
    
    # On affiche la ligne
    print(hivePath)
