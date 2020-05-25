@echo off
SET mypath=%~dp0
cd %mypath:~0,-1%
echo
echo                PPPPPP          CCCCC
echo                PP   PP  oooo  CC    C
echo                PPPPPP  oo  oo CC
echo                PP      oo  oo CC    C
echo                PP       oooo   CCCCC
echo.
echo.
echo UU   UU IIIII PPPPPP    2222    00000   2222    00000
echo UU   UU  III  PP   PP  222222  00   00 222222  00   00
echo UU   UU  III  PPPPPP       222 00   00     222 00   00
echo UU   UU  III  PP        2222   00   00  2222   00   00
echo  UUUUU  IIIII PP       2222222  00000  2222222  00000
echo.
echo.
echo.
echo.
echo %mypath%
echo Installing dependencies...
echo.
pip install flask
pip install requests
pip install pandas
pip install sklearn
pip install influx_logging
pip install timeloop
echo.
echo Done!

echo Starting Servers...
echo.
echo.

cd daten_erheben
cd src
cd data_collection_api
set FLASK_APP=data_collection_api.py
set FLASK_ENV=development
start cmd /k flask run -h localhost -p 4994
cd ../../../

cd daten_bereinigen
cd src
cd bereinigungs_API
set FLASK_APP=bereinigungs_API.py
set FLASK_ENV=development
start cmd /k flask run -h localhost -p 4995
cd ../../../

cd daten_filtern
cd ./src
cd ./filtern_api
set FLASK_APP=filtern_api.py
set FLASK_ENV=development
start cmd /k flask run -h localhost -p 4996
cd ../../../

cd ./daten_klassifizieren
set FLASK_APP=classification_API.py
start cmd /k flask run -h localhost -p 4997
cd ../

cd konfiguration
cd src
set FLASK_APP=config_api.py
set FLASK_ENV=development
start cmd /k flask run -h localhost -p 4998
cd ../../

cd vorhersage_berechnen
cd src
cd prediction_core
cd prediction_api
set FLASK_APP=prediction_api.py
set FLASK_ENV=development
start cmd /k flask run -h localhost -p 4999
cd ../../../../

cd pipeline_controller
cd pipeline_controller_api
set FLASK_APP=pipeline_controller_api.py
set FLASK_ENV=development
start cmd /k flask run -h localhost -p 5000
cd ../../

cd front_end_interface
cd src
cd front_end_interface_api
set FLASK_APP=front_end_interface_api.py
set FLASK_ENV=development
start cmd /k flask run -h localhost -p 5001
cd ../../../

cd ../
cd ui_engine
cd nilan_controller
cd src
cd controller_api
set FLASK_APP=controller_api.py
set FLASK_ENV=development
start cmd /k flask run -h localhost -p 5002
cd ../../../


goto localInflux

:localInflux
    set /p answer2=Do you want your local influx to be setup automatically (Y/N)?
        if /i "%answer2:~,1%" EQU "Y" goto auto
        if /i "%answer2:~,1%" EQU "N" goto remoteInflux
        echo Please type R for remote and L for local
        goto localInflux

:auto
    set /p DUMMY=Please make sure that the bind-adress in your influxDBConfig is set to "127.0.0.1:8088" and press enter.
    set /p answer=Please provide your absolute Influx installation path:
    cd %answer%
    start influxd.exe
    echo Importing nilan database
    influxd restore -portable  %mypath:~0,-1%\schemas\nilan.backup
    echo Done!
    echo Importing db_bereinigte_daten
    influxd restore -portable -db "db_bereinigte_daten" -newdb "db_bereinigte_daten" %mypath:~0,-1%\schemas\db_bereinigte_daten
    echo Importing db_rohdaten
    influxd restore -portable -db "db_rohdaten" -newdb "db_rohdaten"  %mypath:~0,-1%\schemas\db_rohdaten
    echo Importing db_gefilterte_daten
    influxd restore -portable -db "db_gefilterte_daten" -newdb "db_gefilterte_daten" %mypath:~0,-1%\schemas\db_gefilterte_daten
    echo Importing logs
    influxd restore -portable -db "logs" -newdb "logs" %mypath:~0,-1%\schemas\logs
    echo Importing db_klassifizierte_daten
    influxd restore -portable -db "db_klassifizierte_daten" -newdb "db_klassifizierte_daten" %mypath:~0,-1%\schemas\db_klassifizierte_daten
    echo Importing db_vorhersage_daten
    influxd restore -portable -db "db_vorhersage_daten" -newdb "db_vorhersage_daten" %mypath:~0,-1%\schemas\db_vorhersage_daten
    echo Importing db_angereichert_daten
    influxd restore -portable -db "db_angereichert_daten" -newdb "db_angereichert_daten" %mypath:~0,-1%\schemas\db_angereichert_daten
    echo Importing db_markierte_daten
    influxd restore -portable -db "db_markierte_daten" -newdb "db_markierte_daten" %mypath:~0,-1%\schemas\db_markierte_daten
    set /p DUMMY=Database is setup and running on localhost:8086

:remoteInflux
    echo Setup finished!
    echo Please make sure to startup your Influx installation.
    echo Add the connection data in datapipeline/db_connector/src/db_config/db_config.py!
    echo Also check the configuartions provided in datapipeline/konfiguration! Each configuration provides
    echo ways to set databases and measurements to be used in your remote installation!
    set /p DUMMY=Everything else is set you can hit enter to close.
    goto finally

:finally
    cd %mypath:~0,-1%
