cd daten_erheben
cd src
cd data_collection_api
set FLASK_APP=data_collection_api.py
start cmd /k flask run -h localhost -p 4994
cd ../../../

cd daten_bereinigen
cd src
cd bereinigungs_API
set FLASK_APP=bereinigungs_API.py
start cmd /k flask run -h localhost -p 4995
cd ../../../

cd daten_filtern
cd ./src
cd ./filtern_api
set FLASK_APP=filtern_api.py
start cmd /k flask run -h localhost -p 4996
cd ../../../

cd ./daten_klassifizieren
set FLASK_APP=classification_API.py
start cmd /k flask run -h localhost -p 4997
cd ../

cd konfiguration
cd src
set FLASK_APP=config_api.py
start cmd /k flask run -h localhost -p 4998
cd ../../

cd vorhersage_berechnen
cd src
cd prediction_core
cd prediction_api
set FLASK_APP=prediction_api.py
start cmd /k flask run -h localhost -p 4999
cd ../../../../

cd pipeline_controller
cd pipeline_controller_api
set FLASK_APP=pipeline_controller_api.py
start cmd /k flask run -h localhost -p 5000
cd ../../

cd front_end_interface
cd src
cd front_end_interface_api
set FLASK_APP=front_end_interface_api.py
start cmd /k flask run -h localhost -p 5001
cd ../../../