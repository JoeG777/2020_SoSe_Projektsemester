from data_pipeline.exception.exceptions import (
    InvalidTrainingPercentageException,
    RedundantConfigException,
    IncompleteConfigException,
    InconsistentConfigException,
    InvalidConfigException)

import collections
import copy
#TODO changes single quotes to double quotes
def validate_config(config):
    # TODO validate config in general?
    selected_value = config.get("selected_value")

    prediction_units = config.get("prediction_options").get(selected_value)
    check_completeness(prediction_units)
    check_redundancies(prediction_units)
    check_training_percentage(prediction_units)
    check_prediction_chain(prediction_units)


def check_completeness(config):
    to_be_predicted = ['freshAirIntake', 'condenser', 'evaporator', 'outlet', 'room', 'inlet']

    for entry in config:
        if 'dependent' in entry:
            curr_dependent = entry.get('dependent')
            for element in curr_dependent:
                if element in to_be_predicted:
                    to_be_predicted.remove(element)
        else:
            raise InvalidConfigException('An entry of the config does not contain a dependent curve.')
    if to_be_predicted:
        raise IncompleteConfigException('In the current config not every curve is dependent')


def check_redundancies(config):
    to_be_predicted = []

    for entry in config:
        if 'dependent' in entry:
            curr_dependent = entry.get('dependent')
            for element in curr_dependent:
                if element in to_be_predicted:
                    raise RedundantConfigException('Config contains redundant curves.')
                else:
                    to_be_predicted.append(element)
        else:
            raise InvalidConfigException('An entry of the config does not contain a dependent curve.')


def check_prediction_chain(config):
    config = copy.deepcopy(config)
    predicted = ['outdoor']
    to_be_predicted = ['freshAirIntake', 'condenser', 'evaporator', 'outlet', 'room', 'inlet', 'outdoor']

    def compare(x, y): # compare while considering duplicates
        return collections.Counter(x) == collections.Counter(y)

    new_prediction = True

    while new_prediction:
        new_prediction = False

        for entry in config:
            independent_curves = entry.get('independent')
            if all(item in predicted for item in independent_curves):
                dependent_curves = entry.get('dependent')
                predicted = list(set(predicted + dependent_curves))
                new_prediction = True
                config.remove(entry)

    if not compare(predicted, to_be_predicted):
        raise InconsistentConfigException('The prediction chain could not be built fully with the given config!')


def check_training_percentage(config):
    for entry in config:
        if 'test_sample_size' in entry:
            curr_test_sample_size = entry.get('test_sample_size')
            if curr_test_sample_size < 0 or curr_test_sample_size > 1:
                raise InvalidTrainingPercentageException('An entry of the config contains a invalid test sample size: '
                                                         + str(curr_test_sample_size))
        else:
            raise InvalidConfigException('An entry of the config does not contain a test sample size.')


