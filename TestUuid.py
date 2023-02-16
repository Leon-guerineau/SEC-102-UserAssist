import subprocess

def getUuid(inputStr) :
    isUuid = False
    result = ''
    for char in inputStr :
        if (char == '{') :
            isUuid = True
        if(isUuid) :
            result += char
        if (char == '}') :
            isUuid = False
    print(result)

# Chemin des clés de registre UserAssist
userAssistPath = "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist"

# Commande pour lister les clés
result = subprocess.run(f'reg query "{userAssistPath}"', stdout=subprocess.PIPE, shell=True)

keyUuids = []
for line in result.stdout.splitlines():
    decodedLine = line.decode('UTF-8')
    if(decodedLine != ''):
        keyUuids.append(decodedLine)
        getUuid(decodedLine)
print(keyUuids)

