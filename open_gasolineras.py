#!/usr/bin/env python
"""Usage: ./open_gasolineras.py [-d DIR] [-r DIR] [--quiet | --verbose]

-h --help       show this
-d DIR          specify where json output files are saved [default: .]
-r DIR          specify raw output directory [default: .]
-quiet          do not show any debug traces

"""
from docopt import docopt

from shutil import copy
from urllib2 import urlopen, URLError, HTTPError
import os
import zipfile
import json
import re
import requests
import logging

debug_trace = True
output_dir = '.'
raw_output_dir = '.'


def downloadFile(url):
    # Open the url
    try:
        _f = raw_output_dir + '/zip/' + os.path.basename(url)
        if not os.path.exists(_f):
            f = urlopen(url)
            logging.info('downloading' + url)

            # Open our local file for writing
            with open(_f, 'wb') as local_file:
                local_file.write(f.read())

    # handle errors
    except HTTPError, e:
        print('HTTP Error:', e.code, url)
    except URLError, e:
        print('URL Error:', e.reason, url)


def extract(_file):
    _file = raw_output_dir + '/zip/'+_file+'.zip'
    zip_ref = zipfile.ZipFile(_file, 'r')
    zip_ref.extractall(raw_output_dir + '/csv')
    zip_ref.close()
    # os.remove(_file)


def convertCsvToJson(_file):
    _file = raw_output_dir + '/csv/'+_file+'.csv'
    filename = os.path.splitext(os.path.basename(_file))[0]
    logging.info(_file)

    # export file to list
    lines = [line.strip() for line in open(_file)]
    i = 0
    jsonStack = []
    geoJsonStack = []

    # loop thrue lines
    for line in lines:
        i += 1
        # ignore 1st 2 lines
        if i < 3 or line == '':
            continue

        _line = line.split(',', 2)
        _json = {
            'lat': float(_line[0]),
            'lng': float(_line[1]),
            'name': '',
            'price': 0,
        }

        # TEXACO Horario Especial 1,009 e
        if _line[2].find('Horario Especial') != -1:
            matchObj = re.match(
                r'(.*) Horario Especial (\d,\d{3}) e',
                _line[2].strip()[1:]
            )
            if matchObj:
                _json['name'] = matchObj.group(1).strip()
                price = matchObj.group(2).replace(',', '.')
                _json['price'] = float(price)
            else:
                logging.info(' [ Not parsed] ' + line)
        # ESTACION DE SERVICIOS EL  L-D: 24H 0,997 e
        # THADER L-D: 24H 1,309 e
        # BTP L: 06:30-22:30 1,308 e
        else:
            matchObj = re.match(
                r'(.*) .*: .* (\d,\d{3}) e',
                _line[2].strip()[1:]
            )
            if matchObj:
                _json['name'] = matchObj.group(1).strip()
                price = matchObj.group(2).replace(',', '.')
                _json['price'] = float(price)
            else:
                logging.info(' [ Not parsed] ' + line)
        jsonStack.append(_json)
        geoJsonStack.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [_json['lat'], _json['lng']]
            },
            'properties': {
                'name': _json['name'],
                'price': _json['price']
            }
        })

    writeToJson(jsonStack, filename)
    writeToGeoJson({
        "type": "FeatureCollection",
        "features": geoJsonStack
    }, filename)


def writeToGeoJson(object, filename):
    _f = jsonFileName(filename, extraDir='geojson')
    logging.info(' - writing to ' + _f)
    with open(_f, 'w') as outfile:
        json.dump(object, outfile)
    copy(_f, output_dir + '/geojson/latest/')


def writeToJson(object, filename):
    _f = jsonFileName(filename)
    logging.info(' - writing to ' + _f)
    with open(_f, 'w') as outfile:
        json.dump(object, outfile)
    copy(_f, output_dir + '/json/latest/')


def jsonFileName(filename, extraDir='json'):
    matchObj = re.match(r'eess_(\S{3})_(\d{2})(\d{2})(\d{4})', filename)
    _dir = output_dir + '/' + extraDir + '/' + matchObj.group(4) + matchObj.group(3) + matchObj.group(2)
    if not os.path.exists(_dir):
        os.mkdir(_dir)
    return _dir + '/' + matchObj.group(1) + '.json'


def extractZipFilenames():
    url = 'http://geoportal.mityc.es/hidrocarburos/eess/dispmovil.jsp'
    r = requests.get(url)
    files = []
    for line in r.text.split('\n'):
        # <input type="hidden" id="RESTO_G98" name="RESTO_G98" value="eess_G98_04102013.zip" />
        matchObj = re.match(
            r'.*<input.*type="hidden".*id="RESTO_.*".*name="RESTO_.*".*value="(.*).zip" />.*',
            line
        )
        if matchObj:
            files.append(matchObj.group(1))
    return files


def init():
    if not os.path.exists(raw_output_dir + '/csv'):
        os.makedirs(raw_output_dir + '/csv')
    if not os.path.exists(output_dir + '/json/latest'):
        os.makedirs(output_dir + '/json/latest')
    if not os.path.exists(output_dir + '/geojson/latest'):
        os.makedirs(output_dir + '/geojson/latest')
    if not os.path.exists(raw_output_dir + '/zip'):
        os.makedirs(raw_output_dir + '/zip')


def main():
    logging.info('--- initialising')
    init()

    logging.info('\n--- extract zip filenames from html')
    files = extractZipFilenames()

    logging.info('\n--- download zip files')
    for _file in files:
        url = (
            'http://geoportal.mityc.es/'
            'hidrocarburos/files/'
            '%s.zip' % (
                _file,
            )
        )
        downloadFile(url)

    logging.info('\n--- extract zip files')
    for _file in files:
        extract(_file)

    logging.info('\n--- convert csv to json')
    for _file in files:
        convertCsvToJson(_file)

if __name__ == '__main__':
    arguments = docopt(__doc__)
    if not arguments['--quiet']:
        logging.basicConfig(level=logging.INFO)
    output_dir = arguments['-d']
    raw_output_dir = arguments['-r']
    main()