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
            decodedHivePath = hivePath.decode('cp1252')
            if(decodedHivePath != '') :
                hivesPathList.append(decodedHivePath)
        except UnicodeError :
            print('+1 sous clé en erreur de décodage')
    
    # On retourne les sous clés
    return hivesPathList