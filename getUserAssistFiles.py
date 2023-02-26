# Module de gestion de chiffrage/déchiffrage
import codecs

# Module de conversion de binaire
import struct

# Module de gestion de date
import datetime

# Module d'exécution de commandes
import subprocess

# Module pour travailler avec des expressions régulières (regex)
import re



"""
Génère le fichier 'userassist.txt' contenant les valeurs de la clé de registre UserAssist
"""
def generateEncodedUserAssistFile() :

    # La commande pour lister les données de la clé de registre de façon récursive '/s'
    # Le premier \ dans \\ permet d'ajouter le deuxième sans qu'il soit en caractère d'échappement
    userAssistQuery = 'reg query HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist /s'

    # Exécution de la commande
    userAssistQuery = subprocess.run(userAssistQuery, stdout=subprocess.PIPE, shell=True)

    # Écriture des lignes résultantes de la commande dans le fichier userassist.txt
    #   - 'open()' écrase le fichier existant
    with open('userassist.txt', 'wb') as file :

        # '.stdout' permet de récupérer le flux de sortie de la commande exécutée via le module 'subprocess'
        file.write(userAssistQuery.stdout)



"""
Déchiffre et retourne la version de la ruche dans la ligne donnée
    - inputLine :
"""
def getHiveVersion(inputLine) :

    # Récupération numéro de la version en hexadécimal (3ème élément de la ligne)
    encodedVersion = inputLine.split('    ')[2]

    # Conversion du numéro de version en décimal
    version = int(encodedVersion, base=16)

    # Retour de la ligne
    return '\tVersion : ' + str(version) + '\n\n'



"""
Retourne le chemin d'un logiciel décodé en ROT13 pour une ligne donnée
    - encodedProgramPath : le chemin d'un logiciel pouvant contenir un {uuid}
"""
def getDecodedProgramPath(encodedProgramPath) :

    # Recherche de l'uuid
    uuidQueryResult = re.findall('\{.*?\}', encodedProgramPath)
    uuid = uuidQueryResult[0] if uuidQueryResult else ''

    # Isolation du chemin à décoder
    encodedProgramPath = re.sub('\{.*?\}', '', encodedProgramPath)

    # Assemblage de l'uuid suivi du chemin décodé en ROT13
    decodedProgramPath = uuid + codecs.encode(encodedProgramPath, 'rot13')

    return '\t\tChemin du fichier : ' + decodedProgramPath + '\n'



"""
Décompose un nombre de millisecondes donné en h, m, s, ms
    - focusTime : un nombre de millisecondes
"""
def getFormattedFocusTime(focusTime) :

    # Récupération du nombre d'heures
    hours = str(focusTime // 3600000)
    rest = focusTime % 3600000

    # Récupération du nombre de minutes dans le reste
    minutes = str(rest // 60000)
    rest = rest % 60000

    # Récupération du nombre de secondes et de millisecondes le reste
    seconds = str(rest // 1000)
    milliseconds = str(rest % 1000)

    # Retour de la durée
    return str(hours + 'h, ' + minutes + 'm, ' + seconds + 's, ' + milliseconds + 'ms')



"""
Convertit une durée depuis la date de référence du système Windows en date
    - intDateTime : le nombre de centième de seconde depuis la date de référence
"""
def getFormattedDateTime(intDateTime) :

    # Retour d'un message s'il n'y a eu aucune utilisation
    if intDateTime == 0 :
        return 'aucune utilisation'

    # Récupération de la date de référence du système d'exploitation Windows (1er janvier 1601)
    resultDate = datetime.datetime(1601, 1, 1)

    # Ajout de la durée convertie en millisecondes
    resultDate += datetime.timedelta(microseconds=intDateTime/10)

    # Ajout d'une heure pour s'ajuster au fuseau horaire
    resultDate += datetime.timedelta(hours=1)

    # Retour de la ligne
    return str(resultDate)



"""
Déchiffre et retourne les statistiques d'utilisation données
    - encodedStats : Les statistiques chiffrées en hexadécimal
"""
def getDecodedProgramStats(encodedStats) :

    # Découpage en octets
    byteData = bytes.fromhex(encodedStats)

    # Lectures des octets représentants les données
    nbUses = str(struct.unpack('I', byteData[4:8])[0])
    timeFocus = getFormattedFocusTime(struct.unpack('I', byteData[12:16])[0])
    lasTimeUsed = getFormattedDateTime(struct.unpack('Q', byteData[60:68])[0])

    # Mise en forme des lignes
    programStatsLines = '\t\tNombre d\'exécutions sur la session : ' + nbUses + '\n'
    programStatsLines += '\t\tTemps d\'utilisation sur la session : ' + timeFocus + '\n'
    programStatsLines += '\t\tDernière utilisation : ' + lasTimeUsed + '\n\n'

    # Retour des lignes
    return programStatsLines



"""
Déchiffre et retourne les différentes données présentes dans la ligne données d'un logiciel
    - inputLine : la ligne au format '(chemin)    (type de chiffrement)    (données)'
"""
def getProgramData(inputLine) :

    # Division des données de la ligne :
    #   [0] : chemin du logiciel
    #   [1] : type de chiffrement
    #   [2] : statistiques d'utilisation
    encodedData = inputLine.split('    ')

    # Déchiffrage du chemin du logiciel et de ces statistiques d'utilisation
    programPath = getDecodedProgramPath(encodedData[0])
    programStats = getDecodedProgramStats(encodedData[2])

    # Retour des lignes
    return programPath + programStats



"""
Programme Principal
"""

# Génération du fichier 'userassist.txt'
generateEncodedUserAssistFile()

# Ouverture de 'userassist.txt' en lecture et de 'decode_userassist.txt' en écriture
with open('userassist.txt', 'r') as inputFile, open('decode_userassist.txt', 'wb') as outputFile :

    # Parcours des lignes du fichier 'userassist.txt'
    for line in inputFile :

        # Détermine le nombre d'espaces présents au début de la ligne
        nbStartSpaces = len(re.findall(' ', line[:4]))

        # Suppression retour à la ligne '\n' et de de l'indentation '    ' s'il y en a
        line = line[nbStartSpaces:].strip('\n')

        # Traitement du nom de la ruche et exclusion du nom du répertoire '\Count'
        if 'KEY_CURRENT_USER' in line and '}\Count' not in line :
            outputFile.write((line + '\n').encode('utf-8'))

        # Traitement de la ligne de version de la ruche
        elif 'REG_DWORD' in line :
            outputFile.write(getHiveVersion(line).encode('utf-8'))

        # Traitement de la ligne de données d'un logiciel
        elif 'REG_BINARY' in line :
            outputFile.write(getProgramData(line).encode('utf-8'))