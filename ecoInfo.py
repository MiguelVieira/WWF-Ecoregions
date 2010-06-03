import xml.etree.ElementTree as ET
import csv, os

# ecozone codes
_zoneFromZCode = {'aa':'Australasia', 'an':'Antarctica', 'at':'Afrotropic', 'im':'Indomalayan', 'na':'Nearctic', 'nt':'Neotropic', 'oc':'Oceania', 'pa':'Palearctic'}

# process ISO country codes
_countryFromCCode = {}
for c in ET.parse('iso3166.xml').findall('iso_3166_entry'):
    _countryFromCCode[c.get('alpha_2_code').lower()] = c.get('name').encode('utf8')
_countryFromCCode['ci'] = 'Cote d\'Ivoire'

# process ISO country subdivision codes
for c2Elm in ET.parse('iso3166_2.xml').findall('iso_3166_country'):
    for sElms in c2Elm.findall('iso_3166_subset'):
        for sElm in sElms.findall('iso_3166_2_entry'):
            _countryFromCCode[sElm.get('code').lower()] = sElm.get('name').encode('utf8')
                
# process biomes
_biomeFromBCode = {}
for x in csv.reader(open('biomes.csv'), delimiter='\t'):
    _biomeFromBCode[int(x[0])] = x[1]

# process ecoregions
_ecoregionFromECode = {}
_bCodeFromECode = {}
for x in csv.reader(open('ecoregions.csv')):
    code = x[0].lower().strip()
    _bCodeFromECode[code] = int(x[1])
    _ecoregionFromECode[code] = x[2].strip()

def getBCodeFromECode(eCode):
    return _bCodeFromECode[eCode]

# process countries
_eCodesFromCCode = {}
_cCodesFromECode = {}
for x in csv.reader(open('Countries by ecoregion.csv')):
    if 1 < len(x):
        cCode = x[1].lower().strip()
        eCode = x[0].lower().strip()
        if _eCodesFromCCode.has_key(cCode):
            _eCodesFromCCode[cCode].add(eCode)
        else:
            _eCodesFromCCode[cCode] = set([eCode])
        if _cCodesFromECode.has_key(eCode):
            _cCodesFromECode[eCode].add(cCode)
        else:
            _cCodesFromECode[eCode] = set([cCode])
        if 2 < len(cCode):
            code = cCode[0:2]
            if _eCodesFromCCode.has_key(code):
                _eCodesFromCCode[code].add(eCode)
            else:
                _eCodesFromCCode[code] = set([eCode])

def getECodesFromCCode(x):
    return _eCodesFromCCode[x]

def getCCodesFromECode(code):
    return _cCodesFromECode[code]

def toCountryCCode(code):
    return code[0:2]

def getAllCCodes():
    cCodes = [c for c in _eCodesFromCCode.iterkeys() if isCountryCode(c)]
    return cCodes

def getAllECodes():
    return _ecoregionFromECode.keys()

def _isSubdivisionCode(code):
    return len(code) > 2

def isCountryCode(code):
    return len(code) == 2

def _getCountryCode(code):
    if _isSubdivisionCode(code):
        return code[0:code.find('-')]
    else:
        return code      

def getZCodeFromECode(eCode):
    return eCode[0:2]

def _splitByZCode(eCodes):
    result = {}
    for eCode in eCodes:
        zCode = _getZCode(eCode)
        zName = _zoneFromZCode[zCode]
        zTuple = (zCode, zName)
        if result.has_key(zTuple):
            result[zTuple].add(eCode)
        else:
            result[zTuple] = set([eCode])
    return result

def _splitByCCode(eCodes, useSubdivisions):
    result = {}
    for eCode in eCodes:
        for cCode in _cCodesFromECode[eCode]:
            code = cCode[0:2] if not useSubdivisions else cCode
            cTuple = (code, _countryFromCCode[code])
            if result.has_key(cTuple):
                result[cTuple].add(eCode)
            else:
                result[cTuple] = set([eCode])
    return result

def _splitByBCode(eCodes):
    result = {}
    for eCode in eCodes:
        bCode = _bCodeFromECode[eCode]
        bTuple = (bCode, _biomeFromBCode[bCode])
        if result.has_key(bTuple):
            result[bTuple].add(eCode)
        else:
            result[bTuple] = set([eCode])
    return result

def cmpTuples(x, y):
    return cmp(x[1], y[1])

def cmpZCodes(x, y):
    return cmp(getZone(x), getZone(y))

def cmpCCodes(x, y):
    return cmp(getCountry(x), getCountry(y))

def cmpECodes(x, y):
    return cmp(getEcoregion(x), getEcoregion(y))

def cmpBCodes(x, y):
    return cmp(int(x), int(y))

def getBiome(x):
    return _biomeFromBCode[x]

def getEcoregion(x):
    return _ecoregionFromECode[x]

def getZone(x):
    return _zoneFromZCode[x]

def getCountry(x):
    return _countryFromCCode[x]

def getECodesInStates(cCode):
    pred = lambda c: _isSubdivisionCode(c) and c[0:3] == cCode + '-'
    eCodes = [e for e in _eCodesFromCCode.iterkeys() if pred(e)]
    return eCodes
