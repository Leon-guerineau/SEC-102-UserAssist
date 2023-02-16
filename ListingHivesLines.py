import subprocess

# Chemin de la clé de registre UserAssist
userAssistPath = "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist"

# Commande pour lister les sous clés
hivesQuery = subprocess.run(f'reg query "{userAssistPath}"', stdout=subprocess.PIPE, shell=True)

# On parcours, décode et stocke les sous clés résultants de la commande
for hivePath in hivesQuery.stdout.splitlines() :
    
    # Conversion d'UTF-8 à une chaine de caractères banale
    decodedHivePath = hivePath.decode('UTF-8')
    if(decodedHivePath != '') :
        
        # Commande pour lister les lignes du répertoire \count de la sous clé 
        linesQuery = subprocess.run(f'reg query "{decodedHivePath}\\count" /s', stdout=subprocess.PIPE, shell=True)
        
        # On parcours, décode et renvois les résultats de la commande
        for line in linesQuery.stdout.splitlines() :
            decodedLine = line.decode('UTF-8')
            if(decodedLine != '') :
                print(decodedLine)





