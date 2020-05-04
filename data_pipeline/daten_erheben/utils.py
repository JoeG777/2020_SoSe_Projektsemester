from datetime import datetime, timedelta
from influxdb import InfluxDBClient
from console_progressbar import ProgressBar

def get_converted_date(date):

    lastTime = datetime(year = int(date[:4]), month = int(date[5:7]), day = int(date[8:10]), hour = int(date[11:13]), minute = int(date[14:16]), second = int(date[17:19]))
    twoHours = timedelta(hours = 2)

    time = str(lastTime - twoHours)
    timeSplit = time.split(" ")

    returnTime = timeSplit[0] + "T" + timeSplit[1] + "Z"

    return returnTime

def write_to_influx(jsonArray):

    client = InfluxDBClient('localhost', 8086, 'admin', 'admin', 'WetterDWD')
    client.create_database('WetterDWD')

    pbForecast = ProgressBar(total=100,prefix='Daten schreiben', suffix='', decimals=2, length=50, fill='#', zfill='-')
    counter = 1

    for json in jsonArray:
        client.write_points(json)
        percent = float("{:.2f}".format((counter/len(jsonArray)*100)))
        counter += 1
        pbForecast.print_progress_bar(percent)

    print("Daten aktualisiert.")