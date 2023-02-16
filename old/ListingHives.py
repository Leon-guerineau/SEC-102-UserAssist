import subprocess

# Chemin de la clé de registre UserAssist
userAssistPath = "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist"

# Commande pour lister les sous clés
hivesQuery = subprocess.run(f'reg query "{userAssistPath}"', stdout=subprocess.PIPE, shell=True)

# On parcours, décode et renvois les résultats de la commande
for hivePath in hivesQuery.stdout.splitlines() :
    
    # Conversion d'UTF-8 à une chaine de caractères banale
    decodedHivePath = hivePath.decode('UTF-8')
    if(decodedHivePath != '') :
        print(decodedHivePath)


