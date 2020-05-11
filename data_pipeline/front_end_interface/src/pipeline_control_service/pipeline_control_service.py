import data_pipeline.exception.exceptions as exc

def start_process(parameters):

    try:
        pipeline_controller.start_process(parameters)

    except:
        raise exc.DataPipelineException('Unable to start process')

