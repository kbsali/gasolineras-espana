Spain's petrol stations' data
=============================

This is a simple script I created to download the latest oficial price list for all types of petrol for all of the petrol stations in Spain provided by the *Gobierno de España. Ministerio de Industria, Energía y Turismo.* : http://geoportal.mityc.es/hidrocarburos/

* The tool this portal provides is very user *UN*friendly,
* The tool this portal provides is completely *UN*accessible (try to open it up in your mobile phone),
* The data source is somewhat hard to find, and if you do manage to find it, its format is not well structured, making hard to exploit.

This script will :

* *download* the latest zipped data available
 * To do so it parses this "amazing" page : http://geoportal.mityc.es/hidrocarburos/eess/dispmovil.jsp
 * The zip files URLs look something like : http://geoportal.mityc.es/hidrocarburos/files/eess_G98_04102013.zip
* *extract* all the downloaded zip CSV files
* *convert* those CSV to [JSON](http://www.json.org/) and [GEOJSON](http://geojson.org/) format making it much easier to play with.

Ultimately I would like to have a user-friendly (and accessible) solution for users to easily check with any type of browsers (desktop or mobile) where the nearest and cheapest petrol stations are. There are a number of mobile apps available out there (https://play.google.com/store/search?q=gasolineras&c=apps), but all of them are :
* mobile only
* closed source!

Install
-------

```python
wget
pip install requests
chmod +x convert.py
./convert.py
```

See it live!
------------

I have a cron job executing the script daily on my server, use the json files at your own will : http://gas.saliou.name