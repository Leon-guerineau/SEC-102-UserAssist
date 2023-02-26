# Module de gestion de date
import datetime

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
Convertis une durée depuis la date de référence su système Windows en date
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

# Module de conversion de binaire
import struct

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
    programStatsLines = '\t\tNombre d\'exécutions : ' + nbUses + '\n'
    programStatsLines += '\t\tTemps d\'utilisation : ' + timeFocus + '\n'
    programStatsLines += '\t\tDernière utilisation : ' + lasTimeUsed + '\n\n'

    # Retour des lignes
    return programStatsLines

# Affichage du résultat de l'exécution sur une chaine hexadécimale
print(getDecodedProgramStats('010000000100000001000000E60B00002CFAEE3C000080BF000080BF000080BF000080BF000080BF000080BF000080BF000080BF000080BF00000000F0B2E10FDD49D90100000000'))

