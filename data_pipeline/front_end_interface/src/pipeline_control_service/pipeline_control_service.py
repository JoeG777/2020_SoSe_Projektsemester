import data_pipeline.exception.exceptions as exc

def start_process(parameters):
    '''
    Calls the 'start_process'-method in the pipeline controller, which starts the whole forecast process.
    :param parameters:
    :return:
    '''

    try:
        pipeline_controller.start_process(parameters)

    except:
        raise exc.DataPipelineException('Unable to start process')

