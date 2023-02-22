# import des fonctions
from UserAssistFunctions import *

# Le lien de la sous clé
hive = 'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{F4E57C4B-2036-45F0-A9AB-443BCFE33D9F}'

# On récupère et parcourt les lignes de la sous clé
hiveLines = getHiveLines(hive)
for line in hiveLines :
    
    # On affiche la ligne
    print(line)