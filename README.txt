Description

ecoInfo.py is a Python module that functions as a database of biomes, ecozones, countries, and ecoregions based on the WWF's global terrestrial ecoregions. Supporting data is in Ecoregions.csv and biomes.csv. Countries are encoded using ISO 3166 codes, which are in the iso3166*.xml files. These latter files come from pyCountry.

ecoWiki.py uses ecoInfo.py to produce a Wikipedia-formatted table of ecoregions. It was used to produce the List of terrestrial ecoregions (WWF) on Wikipedia.

flickrGroup.py crawls the flickr group Ecoregions of the World and produces a file, eotw.txt, of all the ecoregions tags in the group. It also produces a page of links to photos missing correct ecoregion tags.

ecoFlickr.py consumes the file produced by flickrGroup.py and produces an HTML page of all the ecoregions present in the group as well as a page of all the ecoregions missing from the group.


Installation instructions

These scripts work with Python 2.7.1. ecoInfo.py, ecoWiki.py, and ecoFlickr.py can be run without any setup. ecoFlickr.py takes as input a file named eotw.txt, which is a list of ecoregion codes produced by flickrGroup.py.

flickrGroup.py: Get setuptools and install flickrapi. Also, put your flickr API key in a text file named flickrKey.txt in your working directory.


Contribution guidelines 

Improvemnts appreciated. In particular, Ecoregions.csv, a CSV table of ecoregion-code, country-code pairs, was done by hand and is not perfect. Any corrections would be appreciated.