See my post about the subject : http://kevin.saliou.name/posts/2013-10-22-geojson-carburantes.html

Spain's petrol stations' data
=============================

This is a simple script I created to download the latest oficial price list for all types of petrol of all the petrol stations in Spain provided by the *Gobierno de España. Ministerio de Industria, Energía y Turismo.* : http://www.geoportalgasolineras.es/

* The tool this portal provides is very user *UN* friendly,
* The tool this portal provides is completely *UN* accessible (try to open it up in your mobile phone),
* The data source is somewhat hard to find, and if you do manage to find it, its format is not well structured, making hard to exploit.

This script will :

* *download* the latest zipped data available
 * To do so it parses this "amazing" page
   * http://geoportal.mityc.es/hidrocarburos/eess/dispmovil.jsp
 * The zip files URLs look something like
   * http://geoportal.mityc.es/hidrocarburos/files/eess_G98.zip
* *extract* all the downloaded zip CSV files
 * *extract* the date when the data was generated (first line of each csv file)
* *convert* those CSV to [JSON](http://www.json.org/) and [GEOJSON](http://geojson.org/) format making it much easier to play with.

Ultimately I would like to have a user-friendly (and accessible) solution for users to easily check with any type of browsers (desktop or mobile) where the nearest and cheapest petrol stations are. There are a number of mobile apps available out there (https://play.google.com/store/search?q=gasolineras&c=apps), but all of them are :
* mobile only
* closed source!

Install
-------

```python
pip install -r requirements.txt

wget https://raw.github.com/kbsali/gasolineras-espana/master/open_gasolineras.py
chmod +x open_gasolineras.py

$ ./open_gasolineras.py -h
Usage: ./open_gasolineras.py [-d DIR] [-r DIR] [--quiet | --verbose]

-h --help       show this
-d DIR          specify where json output files are saved [default: .]
-r DIR          specify raw output directory [default: .]
-quiet          do not show any debug traces

./open_gasolineras.py -d /PATH/TO/... --quiet

```

Output
-------

The script will save the json + geojson files in sub directories for each date and an extra *latest* directory so you always have the option to access the latest file easily :

```
├── geojson
│   ├── 20131004
│   │   ├── BIO.geojson
│   │   ├── G98.geojson
│   │   ├── GOA.geojson
│   │   ├── GPR.geojson
│   │   └── NGO.geojson
│   └── latest
│       ├── BIO.geojson
│       ├── G98.geojson
│       ├── GOA.geojson
│       ├── GPR.geojson
│       └── NGO.geojson
└── json
    ├── 20131004
    │   ├── BIO.json
    │   ├── G98.json
    │   ├── GOA.json
    │   ├── GPR.json
    │   └── NGO.json
    └── latest
        ├── BIO.json
        ├── G98.json
        ├── GOA.json
        ├── GPR.json
        └── NGO.json
```

See it live!
------------

I have a cron job executing the script daily on my server, use the json files at your own will : http://gas.saliou.name.
Here are sample files :
* http://gas.saliou.name/geojson/latest/BIO.geojson
* http://gas.saliou.name/json/latest/G98.json

Naming convention
-----------------

I kept the same naming policy as on the original source :
* GPR : Gasolina 95 (G.Protección)
* G98 : Gasolina 98
* GOA : Gasóleo A habitual
* NGO : Nuevo gasóleo A
* GOB : Gasóleo B
* GOC : Gasóleo C
* BIO : Biodiésel
* G95 : Gasolina 95
* BIE : Bioetanol
* GLP : Gases licuados del petróleo
* GNC : Gas natural comprimido