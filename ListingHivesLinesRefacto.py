import subprocess

"""
Fonction qui liste les sous clés de la clé de registre UserAssist
"""
def getHivesPathList() :
    # Chemin de la clé de registre UserAssist
    userAssistPath = "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist"

    # Commande pour lister les sous clés
    hivesQuery = subprocess.run(f'reg query "{userAssistPath}"', stdout=subprocess.PIPE, shell=True)
    hivesQuery = hivesQuery.stdout.splitlines()

    # On parcours, décode et stocke les sous clés résultants de la commande
    hivesPathList = []
    for hivePath in hivesQuery :
        
        # Conversion d'UTF-8 à une chaine de caractères banale
        try :
            decodedHivePath = hivePath.decode('UTF-8')
            if(decodedHivePath != '') :
                hivesPathList.append(decodedHivePath)
        except UnicodeError :
            print('+1 sous clé en erreur de décodage')
    
    # On retourne les sous clés
    return hivesPathList

"""
Fonction qui liste les lignes d'une sous clé donnée
"""
def getHiveLines(hivePath) :
    # Commande pour lister les lignes du répertoire \count de la sous clé 
    linesQuery = subprocess.run(f'reg query "{hivePath}\\count" /s', stdout=subprocess.PIPE, shell=True)
    linesQuery = linesQuery.stdout.splitlines()
    
    # On retire les deux premières lignes car non pertinentes
    linesQuery.pop(0)
    if(len(linesQuery) > 0) :
        linesQuery.pop(0)
    
    # On parcours, décode et renvois les résultats de la commande
    hiveLines = []
    for line in linesQuery :

        # Conversion d'UTF-8 à une chaine de caractères banale
        try :
            decodedLine = line.decode('UTF-8')
            if(decodedLine != '') :
                hiveLines.append(decodedLine)
        except UnicodeError :
            print('+1 ligne en erreur de décodage')
    
    # On retourne les lignes
    return hiveLines
       
"""
Programme Pricipal
"""
hivesPathList = getHivesPathList()
for hivePath in hivesPathList :
    hiveLines = getHiveLines(hivePath)
    if(len(hiveLines) != 0) :
        print(hiveLines)

                