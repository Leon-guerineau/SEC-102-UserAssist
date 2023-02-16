"""
Demo 1 : Listing des sous clés de la clé de registre UserAssist
"""
# import des fonctions
from UserAssistFunctions import *

# On récupère et parcourt les liens des sous clés
hivesPathList = getHivesPathList()
for hivePath in hivesPathList :
    
    # On affiche la ligne
    print(hivePath)