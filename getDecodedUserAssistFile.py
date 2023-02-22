# Module de gestion de chiffrage/déchiffrage
import codecs

from struct import unpack

#Module de gestion de date
import datetime

"""
Extrait un nom de ruche encodée en UTF-8
    - inputLine : la ligne contenant le nom de ruche
"""
def getHiveName(inputLine) :

    # Retour de la ligne
    return (inputLine + '\n').encode('utf-8')

"""

"""
def getHiveVersion(line) :

    # Suppression de l'indentation '    ' et du retour à la ligne '\n'
    line = line[4:].strip('\n')

    # Récupération numéro de la version en hexadécimal (3ème élément de la ligne)
    encodedVersion = line.split('    ')[2]

    # Conversion du numéro de version en décimal
    version = int(encodedVersion, base=16)

    # Retour de la ligne
    return ('\tVersion : ' + str(version) + '\n\n').encode('utf-8')

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


def getFormattedFocusTime(focusTime) :

    hours = str(focusTime // 3600000)
    rest = focusTime % 3600000

    minutes = str(rest // 60000)
    rest = rest % 60000

    seconds = str(rest // 1000)
    milliseconds = str(rest % 1000)

    return str(hours + 'h, ' + minutes + 'm, ' + seconds + 's, ' + milliseconds + 'ms')

"""
"""
def getFormattedDateTime(intDateTime) :
    unix_epoch = datetime.datetime(1601, 1, 1)  # Windows epoch
    delta = datetime.timedelta(hours=1, microseconds=intDateTime/10)

    # Retour de la ligne
    return str(unix_epoch + delta)


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

def getDecodedData(line) :

    encodedData = line.split('    ')[2]
    byteData = bytes.fromhex(encodedData)

    nbUses = str(unpack("I", byteData[4:8])[0])
    timeFocus = getFormattedFocusTime(unpack("I", byteData[12:16])[0])
    lasTimeUsed = getFormattedDateTime(unpack("Q", byteData[60:68])[0])

    return nbUses, timeFocus, lasTimeUsed

def getHiveData(line) :

    line = line[4:].strip('\n')

    path = getDecodedProgramPath(line)
    data = getDecodedData(line)

    result = '\t\tChemin du fichier : ' + path + '\n'
    result += '\t\tNombre d\'exécutions : ' + data[0] + '\n'
    result += '\t\tTemps d\'utilisation : ' + data[1] + '\n'
    result += '\t\tDernière utilisation : ' + data[2] + '\n\n'

    return result.encode('utf-8')

# Overture de 'userassist.txt' en lecture et de 'decode_userassist.txt' en écriture
with open('userassist.txt', 'r') as inputFile, open('decode_userassist.txt', 'wb') as outputFile :

    # Parcours des lignes du fichier 'userassist.txt'
    for line in inputFile :

        # Traitement du nom de la ruche et exclusion du nom du répertoire '\Count'
        if 'KEY_CURRENT_USER' in line and '}\Count' not in line :
            outputFile.write(getHiveName(line))

        # Traitement de la ligne de données
        elif 'REG_BINARY' in line :
            outputFile.write(getHiveData(line))

        # Traitement de la ligne de version
        elif 'REG_DWORD' in line :
            outputFile.write(getHiveVersion(line))