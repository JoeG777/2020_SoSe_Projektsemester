import multiprocessing
import pandas as pd
from datetime import datetime
import data_pipeline.exception.exceptions as exc
import data_pipeline.db_connector.src.read_manager.read_manager as rm
import data_pipeline.db_connector.src.write_manager.write_manager as wm
from data_pipeline.log_writer.log_writer import Logger


# initialize logger
logger = Logger("logs", "cleaning_logs", "uipserver.ddns.net", 8086, "Cleaning_Engine")


def get_data(from_db, from_measurement, value_name, register, time):
    """
    Retrieve data from database
    Name in documentation: get_data
    :param from_db: database from which the data should be extracted
    :param from_measurement: the measurement from which the data should be extracted
    :param value_name: name of the field in influxdb
    :param register: register of the desired curve which should be cleaned
    :param time: tart and end time of the desired period where the curve should be cleaned
    :return: returns temperature data as a Pandas.Series
    """
    query = ""
    if isInt(register):

        query = "SELECT {0} FROM {1} WHERE register='{2}' and time >= {3} and time <= {4}".format(
            value_name, from_measurement, register, time["from"], time["to"])
    else:
        query = "SELECT {0} FROM {1} WHERE time >={2} AND time <={3}".format(
            value_name, from_measurement, time["from"], time["to"])
    return rm.read_query(from_db, query)


def isInt(v):
    try:
        i = int(v)
    except:
        return False
    return True


def write_data(to_db, data, to_measurement):
    """
    Write data to database
    Name in documentation: write_data
    :param to_db: the databasename in which the cleaned data should be written
    :param data: data to be written in the database as a pandas DataFrame
    :param to_measurement: the measurment in which the cleaned data should be written
    """
    # gsons = []
    # index = data.index
    # for i in range(len(data)):
    #     if data.get("temperature")[i]:
    #         json =[{'measurement': "temperature_register",
    #                 "time": str(index[i])[:10] + "T" + str(index[i])[11:19] + "Z",
    #                 "tags": {"register": str(register)},
    #                 "fields": {register: float(data.get("temperature")[i])}
    #                 }]
    #         print(json)
    #         gsons.append(json)
    # wm.write_query_array("testlauf_Datenbereinigung",  gsons)
    wm.write_dataframe(to_db, data, to_measurement)


def format(data):
    """
    Format timestamps to datetime and strip miliseconds
    Name in documentation: format()
    :param data: The data that should be formatted as Pandas.DataFrame
    :return: The formatted data as a Pandas.Series
    :exception NoDataException: Exception is thrown when data is empty
    :exception FormatException: Exception is thrown when timestamps are wrongly formated
    """
    try:
        data.index = data.index.ceil(freq='s')
        data.index = data.index.tz_localize(None)

    except Exception as e:
        raise exc.FormatException("Data format wrong")

    return pd.Series(data.squeeze(), dtype='float64')


def imputation(data, threshold=3600):
    """
    Goes through the dataset and saves a data point and his predecessor in a dictionary if
    the time difference between them is bigger than a given threshold
    Name in documentation: imputation
    :param data: The data that should be checked as Pandas.Series
    :param threshold: The threshold given in second
    :return: The data points as a dictionary
    :exception NoDataException: Exception is thrown when data is empty
    :exception InvalidConfigValueException: Exception which is thrown if the threshold is to low.
    """

    if data.empty:
        raise exc.NoDataException("Data mustn't be empty")
    if threshold < 1:
        raise exc.InvalidConfigValueException('Threshold must be greater than 1.')

    time_index = data.index
    imputation_dict = dict()
    key = 0
    # write points where difference is greater than the threshold into imputation dict
    for i in range(1, len(time_index)):
        diff = (time_index[i] - time_index[i - 1]).total_seconds()
        if diff > threshold:
            value_dict = dict()
            value_dict["from"] = time_index[i - 1].round('min')

            value_dict["to"] = time_index[i].round('min')

            imputation_dict["gap" + str(key)] = value_dict
            key += 1

    return imputation_dict


def rolling_mean(data, frame_width=100):
    """
    Name in documentation: rolling_mean()
    Applies the rolling mean on the data based on a given frame width
    Name in documentation: rolling_mean
    :param data: The data on which the rolling mean should be applied on as a pandas Series
    :param frame_width: The window width that should be used for the rolling mean
    :return: The data on which the rolling mean was applied on
    :exception NoDataException: Exception is thrown when data is empty
    :exception InvalidConfigValueException: Exception which is thrown if the framewidth is to low.
    """

    if data.empty:
        raise exc.NoDataException("Data mustn't be empty")
    if frame_width < 0:
        raise exc.InvalidConfigValueException('Framewidth cannot be less than 0 ')

    return data.rolling(frame_width).mean()


def resample(data, freq='60S'):
    """
    Method to resample the given data with the given frequency. This is necessary for an union time intervall.
    Name in documentation: resample
    :param data: given data as pandas Series which should be resampled in this method.
    :param freq: A frequency, needed for the resampling, it is used to generate the union time intervall.
    :return dsata.resample(freq).asfreq(): resampled data with an union time intervall as a pandas Series.
    :exception NoDataException: Exception is thrown when data is empty
    :exception InvalidConfigValueException: Exception which is thrown if the frequency is to low.
    """
    if data.empty:
        raise exc.NoDataException("Data mustn't be empty")
    if int(freq[:-1]) < 1:
        raise exc.InvalidConfigValueException('Resample frequency cannot be less than 1S')

    data = data[~data.index.duplicated()]
    return data.resample(freq).asfreq()


def interpolation(data):
    """
    Method to interpolate the given data (resampled data) with an cubic interpolation, which is used to fill the gaps
    made in the resample() method
    Name in documentation: interpolation
    :param data: given data as a pandas Series which should be interpolated in this method, should be resampled before
    :return data.interpolate(): interpolated data without gaps.
    :exception NoDataException: Exception is thrown when data is empty
    """
    if data.empty:
        raise exc.NoDataException("Data mustn't be empty")

    return data.interpolate(method='cubic')


def cut(data, time_from, time_to):
    """
    Method to set the timestamps in any time interval to NaN, from an giving start date to an giving end date.
    :param data: given data as pandas Series in which a time interval should be cutted, shoud be interpolated before.
    :param time_from: timestamp from the start date where the timestamps should be started to cut.
    :param time_to: timestamp from the end date where the timestamps should be ended to cut.
    :return: data: cutted data with NaN timestamps at the desired time interval
    """
    data[time_from: time_to] = float("NaN")
    return data


def remove_gaps(data, imputation_dict):
    """
    Method to remove the gaps of the given data which are found out in the imputation() method
    :param data: whole interpolated data as pandas Series in which the gaps should be cutted
    :param imputation_dict: dictionary of gaps which contains the timestamps of the found gaps. If no gaps were found,
    remove_gaps has no effect.
    :return data: cut data with NaN timestamps at the given time intervalls from the imputation_dict
    :exception NoDataException: Exception is thrown when data is empty
    :exception ImputationDictionaryException: Exception is thrown when no Imputation Dictionary is given
    """

    # Using the implicit booleanness of the empty list is quite pythonic
    if data.empty:
        raise exc.NoDataException("Data mustn't be empty")
    if imputation_dict is None:
        raise exc.ImputationDictionaryException("Imputation Dictionary mustn't be None")

    # set values between gaps to NaN with cut function
    for i in range(len(imputation_dict)):
        cut(data, imputation_dict["gap" + str(i)]["from"], imputation_dict["gap" + str(i)]["to"])

    return data


def craft(data, value_name, register):
    """convert the pandas Series to a pandas DataFrame and add the right column name
    :param data: data as pandas Series which should be converted to a pandas DataFrame
    :param value_name: the value name which should changed to the value of the register param
    :param register: the value as a int if the register is from the sensordata else a given colum name as string
    """
    if isInt(register):
        if int(register) == 201:
            register = "freshAirIntake"
        elif int(register) == 202:
            register = "inlet"
        elif int(register) == 204:
            register = "outlet"
        elif int(register) == 205:
            register = "condenser"
        elif int(register) == 206:
            register = "evaporator"
        elif int(register) == 210:
            register = "room"

    res = pd.DataFrame(data)
    res = res.rename(columns={value_name: register})
    return res.where((pd.notnull(res)), None)


def workflow(from_db, to_db, from_measurement, to_measurement, value_name, register, frame_width, freq, threshold,
             time):
    """
    Method to coordinate the workflow of the execution of methods in this file
    :param from_db: database from which the data should be extracted
    :param to_db: dataabase in which should be written
    :param from_measurement: the measurement from which the data should be extracted
    :param to_measurement: the measurement in which should be written
    :param value_name: name of the field in influxdb
    :param register: register of the desired curve which should be cleaned
    :param frame_width: Value that specifies how smooth the rolling_mean() method makes the curve
    :param freq: A frequency, needed for the resampling, it is used to generate the union time intervall.
    :param threshold: Value that specifies if an gap is to big to interpolate and have to be remove
    :param time: start and end time of the desired period where the curve should be cleaned
    :exception DBError: Exception maybe is thrown from get_data() and write_data()
    :exception NoDataException: Exception is thrown when data is empty
    :exception FormatException: Exception is thrown when timestamps are wrongly formated
    :exception ImputationDictionaryException: Exception is thrown when no Imputation Dictionary is given
    :exception InvalidConfigException: Exception is thrown when Config structure is faulty
    """

    try:
        raw_data_series = get_data(from_db, from_measurement, value_name, register, time)
        print("Daten geholt")

        formated = format(raw_data_series)
        print("daten formatiert")

        imputation_dict = imputation(formated, threshold)
        print("daten imputiert")

        rolling = rolling_mean(formated, frame_width)
        print("Gleitender Mittelwert gebildet")

        resampled = resample(rolling, freq)
        print("Daten resampled")

        interpolated = interpolation(resampled)
        print("Daten interpoliert")

        without_gaps = remove_gaps(interpolated, imputation_dict)
        print("lücken entfernt")

        final = craft(without_gaps, value_name, register)

        write_data(to_db, final, to_measurement)
        print("Daten bereinigt")

    except exc.DBException as dbe:
        logger.error(dbe.args[0])
        raise dbe
    except exc.NoDataException as nde:
        logger.error(nde.args[0])
        raise nde
    except exc.FormatException as fe:
        logger.error(fe.args[0])
        raise fe
    except exc.ImputationDictionaryException as ide:
        logger.error(ide.args[0])
        raise ide
    except exc.InvalidConfigKeyException as icke:
        logger.error(icke.args[0])
        raise icke
    except exc.InvalidConfigValueException as icve:
        logger.error(icve.args[0])
        raise icve


def fast_and_furious(from_db, to_db, from_measurement, to_measurement, value_name, register, frame_width, freq,
                     threshold, time):
    # (from_db, to_db, from_measurement, to_measurement, value_name, register, frame_width, freq, threshold, time)
    """
    for enhanced runtime this function splits the cleaning workflow into different processes, one process per register
    :param from_db: database from which the data should be extracted
    :param to_db: dataabase in which should be written
    :param from_measurement: the measurement from which the data should be extracted
    :param to_measurement: the measurement in which should be written
    :param value_name: name of the field in influxdb
    :param register: register of the desired curve which should be cleaned
    :param frame_width: Value that specifies how smooth the rolling_mean() method makes the curve
    :param freq: A frequency, needed for the resampling, it is used to generate the union time intervall.
    :param threshold: Value that specifies if an gap is to big to interpolate and have to be remove
    :param time: start and end time of the desired period where the curve should be cleaned
    """
    curves = [v.strip() for v in register.split(',')]
    procs = []
    for i in range(len(curves)):
        proc = multiprocessing.Process(target=workflow,
                                       args=(from_db, to_db, from_measurement, to_measurement,
                                             value_name, curves[i], frame_width, freq, threshold, time))
        procs.append(proc)

        proc.start()
    for proc in procs:
        proc.join()


if __name__ == "__main__":
    # TEST#
    # fast_and_furious("valueScaled", "temperature_register", "historic",
    #                 {"from": "1478268800189003008", "to": "1678268811144129024"}, 3600, 10, "60S")

    fast_and_furious("nilan", "testlauf_Datenbereinigung", "temperature_register", "temperature_register",
                     "valueScaled", "201", 10, "60S", 3600, {"from": "1578268800189003008", "to": "1578270018458657024"})