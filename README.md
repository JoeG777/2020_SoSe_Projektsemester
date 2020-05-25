# Machine learning-Based Predictive Analytics of Time Series Data for Visualization and Process Control
Distributed service-oriented architecture (DSOA) for analysing and predicting events based on timeseries data. This application was developed for the ventilation system Nilan Combi S 302 Polar Top. It generates models by analysing historic sensor data which enables predicting machine behaviour based on forecast weather data.

# Prerequisites
Python 3.7, all required dependencies will be imported when starting <b>start.bat.<b>
Grafana for visualization dashboards.
InfluxDB as database.

# Platform
Tested on: 
Windows 10
MacOS 

# Usage
To set up the system run dev.bat and db.bat file in order to create all necessary Grafana dashboards and databases. Make sure ports 4994 to 5002 are not occupied. These ports will be used for the webservers to run on. After starting the webservers using start.bat the user can interact with the system by using web hosted client application. To any given time, system configuration parameters may be adjusted using the config.py files. 
First setup may take several minutes as all historic data will be gathered and processed. Since data collection works periodically it is recommended to run system permanently.
 
# Structure
* data_pipeline
  - `daten_bereinigen`		  contains all scripts needed for data cleaning purposes
  - daten_erheben		        contains all scripts needed for data gathering purposes
  - daten_filtern			      contains all scripts need for data filtering purposes
  - daten_klassifizieren		contains all scripts need for data classification purposes
  > vorhersage_berechnen	contains all scripts to provide prediction data
  > db_connector			manages all read and write-accesses to databases
  > exception			provide exception handling
  > front_end_interface		interface to access frontend
  > configuration			allows to modify system behaviour
  > log_writer			enables exception logging to database
  > pipeline_controller		core component that orchestrates workflow of services
  > dev.bat			initializes dashboards with saved settings
  > start.bat			starts webservices 
> ui_engine
	> nilan_controller		contains all scripts for web-client visualization 
> README.md				

# Acknowledgement
Grafana		https://github.com/grafana/grafana
InfluxDB		https://github.com/influxdata/influxdb

# Author
UIP Sommer Semester 2020
root@uipserver.ddns.net

