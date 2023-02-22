# Module d'exécution de commandes
import subprocess

# La commande pour lister les données de la clé de registre de façon recursive '/s'
# Le premier \ dans \\ permet d'ajouter le deuxième sans qu'il soit en caractère d'échappement
userAssistQuery = 'reg query HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist /s'

# Exécution de la commande
userAssistQuery = subprocess.run(userAssistQuery, stdout=subprocess.PIPE, shell=True)

# Écriture des lignes résultantes de la commande dans le fichier userassist.txt
#   - 'open()' écrase le fichier existant
with open('userassist.txt', 'wb') as file :

    # '.stdout' permet de récupéré le flux de sortie de la commande exécutée via le module 'subprocess'
    file.write(userAssistQuery.stdout)
