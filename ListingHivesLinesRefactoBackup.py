from getHivesPathList import getHivesPathList
import subprocess
import codecs
from struct import unpack


"""
Fonction qui liste les lignes d'une sous clé donnée
    - hivePath : le chemin de la sous clé
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
        
        # Conversion de cp1252 à une chaine de caractères banale
        try :
            decodedLine = line.decode('cp1252')
            if(decodedLine != '') :
                hiveLines.append(decodedLine)
        except UnicodeError :
            print('+1 ligne en erreur de décodage')
            
    # On retourne les lignes
    return hiveLines



"""
Fonction qui récupère l'uuid d'une chaine de caractères
    - inputStr : la chaine de caractères
"""
def getUuid(inputStr) :
    isUuid = False
    result = ''
    for char in inputStr :
        
        # Si le caractère est { alors ce caratère et les caratères suivant font partie de l'uuid
        if (char == '{') :
            isUuid = True
            
        # Si le caractère fait partie de l'uuid alors on le stocke
        if(isUuid) :
            result += char
            
        # Si le caractère est } alors les caratères suivant ne font pas partie de l'uuid
        if (char == '}') :
            isUuid = False
            
    # On retourne l'uuid ou une chaine vide
    return result



"""
Fonction qui retire l'uuid contenu dans une chaine de caractères s'il y en a un
    - inputStr : la chaine de caractères
"""
def removeUuid(inputStr) :
    uuid = getUuid(inputStr)
    
    # S'il y a un uuid alors on le retire et on retourne la chaine
    if(uuid != '') :
        return inputStr.replace(uuid, "")
    
    # Sinon on retourne la chaine non changée
    else :
        return inputStr


"""
Fonction qui retourne le chemin d'un logiciel pour une ligne donnée
    - line : la ligne au format '    (chemin)    (type)    (données)'
    - decoded : booléen déterminant si le résultat est décodeé en rot 13 (vrai par défaut)
"""
def getProgramPath(line, decoded = True) :
    splittedLine = line.split('    ')
    
    # On retire le premier élément qui est créé par la tabulation en début de ligne
    if(splittedLine[0] == '') :
        splittedLine.pop(0)
    programPath = removeUuid(splittedLine[0])
    
    if(decoded) :
        # On retourne le chemin déchiffré en rot13
        print(codecs.encode(programPath, 'rot13'))
        return codecs.encode(programPath, 'rot13')
    else :
        return programPath
    
    
    
def getData(line, decoded = True) :
    result = ''
    splittedLine = line.split('    ')
    
    # On retire le premier élément qui est créé par la tabulation en début de ligne
    if(splittedLine[0] == '') :
        splittedLine.pop(0)
    data = removeUuid(splittedLine[2])
    byteData = bytes.fromhex(data)
    result += '		Nombre d\'éxécutions : ' + str(unpack("I", byteData[4:8])[0]) + '\n'
    result += '		Temps d\'utilisation : ' + str(unpack("I", byteData[12:16])[0]) + '\n'
    result += '		Date de la dernière éxécution : ' + str(unpack("I", byteData[12:16])[0]) + '\n'
    return result
    # print(unpack("I", byteData[4:8])[0], unpack("I", byteData[12:16])[0], unpack("Q", byteData[60:68])[0])

"""
Programme Pricipal
"""
encodedData = []
decodedData = []

# On récupère et parcourt les liens des sous clés
hivesPathList = getHivesPathList()
for hivePath in hivesPathList :
    
    # On récupère et parcourt les lignes de la sous clé si elle en a
    hiveLines = getHiveLines(hivePath)
    if(len(hiveLines) != 0) :
        
        # Ajout du chemin de la sous clé
        encodedData.append(hivePath+'\n')
        decodedData.append(hivePath+'\n')
        
        # Ajout des liens de programmes
        for line in hiveLines :
            encodedData.append('	'+getProgramPath(line, False))
            decodedData.append('	'+getProgramPath(line))
            decodedData.append(getData(line))
        
        # Ajout d'une ligne pour faire un saut de ligne
        encodedData.append('')
        decodedData.append('')

# Écriture des données encodés dans le fichier userassist.txt
with open("userassist.txt", "wb") as file:
    file.write("\n".join(encodedData).encode('utf-8'))

# Écriture des données décodés dans le fichier decode_userassist.txt
with open("decode_userassist.txt", "wb") as file:
    file.write("\n".join(decodedData).encode('utf-8'))

                