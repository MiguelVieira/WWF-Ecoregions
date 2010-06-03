import os, ecoInfo

def ahref(link, text):
    return '<a href=\"' + link + '\">' + text + '</a>'

def br():
    return '<br>'

def printCCodeFlickr(code):
    return '<b>' + ecoInfo.getCountry(code) + '</b><br>'

def printBCodeFlickr(code):
    return '<i>' + ecoInfo.getBiome(code) + '</i><br>'

def flickrLink(eCode):
    eTag = ecoInfo.getEcoregion(eCode).replace(' ','').replace('-','').replace('.','')
    prefix = 'http://www.flickr.com/search/groups/?m=pool&w=1334707%40N21&q='
    link = prefix + eTag
    return link

def wwfLink(eCode):
    ecozone = eCode[0:2]
    prefix = 'http://www.worldwildlife.org/wildworld/profiles/terrestrial/'
    suffix = '_full.html'
    link = prefix + ecozone + '/' + eCode + suffix
    return link

def printECodeFlickr(code, printFlickrLink):
    if printFlickrLink:
         return ahref(flickrLink(code), ecoInfo.getEcoregion(code)) + ' ' + ahref(wwfLink(code), '(WWF full report)') + '<br>'
    else:
         return ahref(wwfLink(code), ecoInfo.getEcoregion(code)) + '<br>'

def printHtmlBoilerplateBegin():
    return '<html><head><title>Pictures of the terrestrial ecoregions of the world</title><body bgcolor=#FFFFFF text=#000000><font face="Arial, Tahoma, Verdana">'

def printHtmlBoilerplateEnd():
    return '</body></html>'        

def getTuples(eCodes, cFilter, transform):
    result = set()
    for eCode in eCodes:
        for cCode in ecoInfo.getCCodesFromECode(eCode):
            if cFilter(cCode):
                cCode = transform(cCode)
                bCode = ecoInfo.getBCodeFromECode(eCode)
                result.add((cCode, bCode, eCode))

    def mySort(x, y):
        cmpC = ecoInfo.cmpCCodes(x[0], y[0])
        if cmpC != 0:
            return cmpC

        cmpB = ecoInfo.cmpBCodes(x[1], y[1])
        if cmpB != 0:
            return cmpB

        return ecoInfo.cmpECodes(x[2], y[2])

    result = list(result)
    result.sort(mySort)
    return result
    
def printFlickrPage(tuples, dst, printFlickrLink):
    with open(dst, 'w') as f:
        cCode = tuples[0][0]
        bCode = tuples[0][1]
        eCode = tuples[0][2]
        f.write(printHtmlBoilerplateBegin())
        f.write(printCCodeFlickr(cCode))
        f.write(printBCodeFlickr(bCode))
        f.write(printECodeFlickr(eCode, printFlickrLink))
        for entry in tuples[1:]:
            cCodeTemp = entry[0]
            bCodeTemp = entry[1]
            if cCodeTemp != cCode:
                cCode = cCodeTemp
                bCode = bCodeTemp
                f.write('<br>')
                f.write(printCCodeFlickr(cCode))
                f.write(printBCodeFlickr(bCode))
            elif bCodeTemp != bCode:
                bCode = bCodeTemp
                f.write('<br>')
                f.write(printBCodeFlickr(bCode))
            eCode = entry[2]
            f.write(printECodeFlickr(eCode, printFlickrLink))
        f.write(printHtmlBoilerplateEnd())
        
def getMissingECodes(eCodes):
    eCodesSet = set(eCodes)
    result = set()
    for e in ecoInfo.getAllECodes():
        if not e in eCodesSet:
            result.add(e)
    return result


def truePred(x):
    return True

def noAction(x):
    return x

eCodesAvailable = [e.strip().lower() for e in file.readlines(open('eotw.txt'))]
tuples = getTuples(eCodesAvailable, truePred, lambda c: c[0:2])
printFlickrPage(tuples, 'ecoregions.html', True)

eCodesMissing = getMissingECodes(eCodesAvailable)
tuples = getTuples(eCodesMissing, truePred, lambda c: c[0:2])
printFlickrPage(tuples, 'missing-ecoregions.html', False)

tuples = getTuples(eCodesAvailable, lambda c: c.find('us-') >= 0, noAction)
printFlickrPage(tuples, 'united-states-ecoregions.html', True)

tuples = getTuples(eCodesAvailable, lambda c: c.find('in-') >= 0, noAction)
printFlickrPage(tuples, 'india-ecoregions.html', True)

tuples = getTuples(eCodesAvailable, lambda c: c.find('ca-') >= 0, noAction)
printFlickrPage(tuples, 'canada-ecoregions.html', True)
