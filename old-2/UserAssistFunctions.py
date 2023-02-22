import subprocess
import codecs

"""
Enregistre les données non déchiffrés de la clé de registre dans le fichier userassist.txt
"""
def getUserAssistFile() :
    # Chemin de la clé de registre UserAssist
    userAssistPath = "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist"

    # Commande pour lister les sous clés et leurs données (/s)
    userAssistQuery = subprocess.run(f'reg query "{userAssistPath}" /s', stdout=subprocess.PIPE, shell=True)

    # Écriture des données dans le fichier userassist.txt
    with open("userassist.txt", "wb") as file:
        file.write(userAssistQuery.stdout)



"""
Liste les sous clés de la clé de registre UserAssist
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



"""
Liste les lignes d'une sous clé donnée
    - hivePath : le chemin de la sous clé
"""
def getHiveLines(hivePath) :
    # Commande pour lister les lignes du répertoire \count de la sous clé 
    linesQuery = subprocess.run(f'reg query "{hivePath}\\count" /s', stdout=subprocess.PIPE, shell=True)
    linesQuery = linesQuery.stdout.splitlines()
    
    # On retire les deux premières lignes car elles sont non pertinentes
    linesQuery.pop(0)
    if(len(linesQuery) > 0) :
        linesQuery.pop(0)
    
    # On parcours, décode et renvois les résultats de la commande
    hiveLines = []
    for line in linesQuery :
        
        # Conversion de cp1252 à une chaîne de caractères banale
        try :
            decodedLine = line.decode('cp1252')
            if(decodedLine != '') :
                
                # Le [4:] permet d'enlever les 4 premiers espaces au début de la ligne
                hiveLines.append(decodedLine[4:])
        except UnicodeError :
            print('+1 ligne en erreur de décodage')
            
    # On retourne les lignes
    return hiveLines



"""
Retourne l'uuid d'une chaine de caractères
    - inputStr : la chaine de caractères
"""
def getUuid(inputStr) :
    isUuid = False
    result = ''
    for char in inputStr :
        
        # Si le caractère est { alors ce caractère et les caractères suivant font partie de l'uuid
        if (char == '{') :
            isUuid = True
            
        # Si le caractère fait partie de l'uuid alors on le stocke
        if(isUuid) :
            result += char
            
        # Si le caractère est } alors les caractères suivant ne font pas partie de l'uuid
        if (char == '}') :
            isUuid = False
            
    # On retourne l'uuid ou une chaine vide
    return result


"""
Fonction qui retourne le chemin d'un logiciel décodé en ROT13 pour une ligne donnée
    - line : la ligne au format '    (chemin)    (type)    (données)'
"""
def getDecodedProgramPath(line) :

    # On récupère le chemin encodé et son uuid
    encodedProgramPath = line.split('    ')[0]
    uuid = getUuid(encodedProgramPath)

    # S'il y a un uuid alors on le retire
    if(uuid != '') :
        encodedProgramPath = encodedProgramPath.replace(uuid, '')

    # On retourne l'uuid suivi du chemin décodé en ROT13
    return uuid + codecs.encode(encodedProgramPath, 'rot13')

# def getDecodedLineData(line) :

