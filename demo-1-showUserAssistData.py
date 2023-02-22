# Module d'exécution de commandes
import subprocess
# Module pour travailler avec les encodages
import codecs

# La commande pour lister les données de la clé de registre de façon recursive '/s'
# Le premier \ dans \\ permet d'ajouter le deuxième sans qu'il soit en caractère d'échappement
userAssistQuery = 'reg query HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist /s'

# Exécution de la commande
userAssistQuery = subprocess.run(userAssistQuery, stdout=subprocess.PIPE, shell=True)

# Affichage du résultat
#   - '.stdout' permet de récupéré le flux de sortie de la commande exécutée via le module 'subprocess'
#   - '.decode('cp1252')' permet de retirer l'encodage par défaut du système windows (pour la demo)
print(userAssistQuery.stdout.decode('cp1252'))