import flickrapi
import xml.etree.ElementTree as ET
import pickle
import ecoInfo
import string

with open('flickrKey.txt', 'r') as f:
	key = f.readline()
groupId = '1334707@N21'

flickr = flickrapi.FlickrAPI(key)

def getTags(photoXml):
    return [tag.text for tag in photoXml.find('tags')]

def getUrl(photoXml):
    return photoXml.find('urls').find('url').text

def getPhoto(photoId):
    return flickr.photos_getInfo(api_key = key, photo_id = photoId)[0]

def getGroupPhotos(groupId, pageIndex, photoCount):
    print "getGroupPhotos page " + str(pageIndex)
    return flickr.groups_pools_getPhotos(group_id = groupId, page = pageIndex, per_page = photoCount)[0]
    
def getPhotoIds(groupXml):
    return [p.attrib['id'] for p in groupXml]

def getPageCount(groupXml):    
    return int(groupXml.attrib['pages'])

def getPhotosIdsFromApi():
    photoCount = 500
    page = 1
    pageXml = getGroupPhotos(groupId, page, photoCount)

    pageCount = getPageCount(pageXml)

    photoIds = getPhotoIds(pageXml)
    for pageIndex in range(2, pageCount + 1):
        photoIds.extend(getPhotoIds(getGroupPhotos(groupId, pageIndex, photoCount)))

    picklePhotoIds(photoIds)

    return photoIds

def normalizeEcoregion(e):
    e = e.lower().replace(' ', '').replace('-','').replace(',','').replace('.','')
    e = filter(lambda x: x in string.printable, e)
    return e

pickleFile = "pickle.bin"

def unpicklePhotoIds():
    return pickle.load(open(pickleFile))

def picklePhotoIds(photoIds):
    pickle.dump(photoIds, open(pickleFile, "wb"))

def isEcoregion(tag):
    return normalizeEcoregion(tag) in normalizedEcoregions

def ecoregionsInTags(tags):
    return filter(isEcoregion, tags)

def getECodes(ecoregions):
    return [normalizedEcoregions[normalizeEcoregion(e)] for e in ecoregions]


normalizedEcoregions = dict()
for c in ecoInfo.getAllECodes():
    ecoregion = ecoInfo.getEcoregion(c)
    normalizedEcoregions[normalizeEcoregion(ecoregion)] = c

photoIds= getPhotosIdsFromApi()
        
badPhotos = list()
eCodes = set()

count = 1
max = 10000
for photoId in photoIds:
    print "processing photo " + str(count) + " of " + str(len(photoIds))
    count = count + 1
    if (count >= max):
        break
    photoXml = getPhoto(photoId)
    tags = getTags(photoXml)
    ecoregions = ecoregionsInTags(tags)
    if (len(ecoregions) == 0):
        badPhotos.append(photoId)
    else:
        [eCodes.add(c) for c in getECodes(ecoregions)]

f = open('eotw.txt', 'w')
for e in eCodes:
    f.write(e + '\n')
f.close()

f = open('badPhotos.html', 'w')
for b in badPhotos:
    url = getUrl(getPhoto(b))
    f.write("<a href =\"" + url + "\">" + url + "</a><br/>" + '\n')
f.close()












