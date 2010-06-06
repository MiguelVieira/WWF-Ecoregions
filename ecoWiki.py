import ecoInfo

def getCountryWiki(x):
    if x == 'us-ga':
        return 'Georgia (U.S. state)|Georgia'
    if x == 'in-pb':
        return 'Punjab (India)'
    if x == 'in-ul':
        return 'Uttaranchal'
    if x == 'in-py':
        return 'Puducherry'
    if x == 'us-wa':
        return 'Washington (U.S. state)|Washington'
    if x == 'cg':
        return 'Republic of the Congo'
    if x == 're':
        return 'Réunion'
    if x == 'ge':
        return 'Georgia (country)|Georgia'
    else:
        return ecoInfo.getCountry(x)

def getEcoregionWiki(x):
    ecoregion = ecoInfo.getEcoregion(x)
    if ecoregion == 'Chaco':
        return 'Chaco (WWF ecoregion)'
    else:
        return ecoregion

def printWiki(cCodes, dst):
    result = []
    for cCode in cCodes:
        for eCode in ecoInfo.getECodesFromCCode(cCode):
            bCode = ecoInfo.getBCodeFromECode(eCode)
            zCode = ecoInfo.getZCodeFromECode(eCode)
            result.append((zCode, bCode, eCode, cCode))

    def mySort(x, y):
        cmp0 = ecoInfo.cmpZCodes(x[0], y[0])
        if cmp0 != 0:
            return cmp0

        cmp1 = ecoInfo.cmpBCodes(x[1], y[1])
        if cmp1 != 0:
            return cmp1

        cmp2 = ecoInfo.cmpECodes(x[2], y[2])
        if cmp2 != 0:
            return cmp2

        return ecoInfo.cmpCCodes(x[3], y[3])
      
    with open(dst, 'w') as f:
        f.write('{| class="wikitable sortable"\n')
        f.write('| \'\'\'[[Ecozone]]\'\'\'\n')
        f.write('| \'\'\'[[Biome]]\'\'\'\n')
        f.write('| \'\'\'[[Ecoregion]]\'\'\'\n')
        f.write('| \'\'\'Country\'\'\'\n')
        for entry in sorted(result, mySort):
            f.write('|-\n')
            f.write('| [[' + ecoInfo.getZone(entry[0]) + ']]\n')
            f.write('| [[' + ecoInfo.getBiome(entry[1]) + ']]\n')
            f.write('| [[' + getEcoregionWiki(entry[2]) + ']]\n')
            f.write('| [[' + getCountryWiki(entry[3]) + ']]\n')
        f.write('|}\n')                        

#pred = lambda c: len(c) == 2
cCodes = ecoInfo.getAllCCodes()
printWiki(cCodes, 'wiki.txt')
