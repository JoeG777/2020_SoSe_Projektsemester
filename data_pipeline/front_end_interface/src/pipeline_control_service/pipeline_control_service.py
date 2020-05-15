import data_pipeline.exception.exceptions as exc
import data_pipeline.log_writer.log_writer as log_writer

logger = log_writer.Logger()

def start_process(parameters):
    '''
    Calls the 'start_process'-method in the pipeline controller, which starts the whole forecast process.
    :param parameters: Parameters from Usersettings in the Web-application
    '''

    try:
        pipeline_controller.start_process(parameters)

    except:
        logger.influx_logger.error('Unable to start process')
        raise exc.RawDataException('Unable to start process', 905)

