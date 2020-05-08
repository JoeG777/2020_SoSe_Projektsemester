from data_pipeline.exception.exceptions import *

import collections
import copy
from numbers import Number


# TODO change single quotes to double quotes
def validate_config(config):
    if isinstance(config, dict):
        check_general_constraints(config)

        selected_value = config.get("selected_value")

        prediction_units = config.get("prediction_options").get(selected_value)
        check_completeness(prediction_units)
        check_redundancies(prediction_units)
        check_training_percentage(prediction_units)
        check_prediction_chain(prediction_units)
    else:
        raise ConfigTypeException("Config is of wrong type: " + str(type(config)))


def check_general_constraints(config):
    # TODO this should be refactored
    valid_independent_values = ['outdoor', 'freshAirIntake', 'condenser', 'evaporator', 'outlet', 'room', 'inlet']
    valid_dependent_values = ['freshAirIntake', 'condenser', 'evaporator', 'outlet', 'room', 'inlet']

    option_found = False

    if "selected_value" in config:
        selected_value = config["selected_value"]

        if "prediction_options" in config:
            prediction_options = config["prediction_options"]

            if isinstance(prediction_options, dict):
                for key in prediction_options:
                    if key == selected_value:
                        prediction_units = prediction_options.get(key)
                        option_found = True

                        if isinstance(prediction_units, list):
                            for prediction_unit in prediction_units:
                                if isinstance(prediction_unit, dict):
                                    if ("independent" in prediction_unit
                                            and "dependent" in prediction_unit
                                            and "test_sample_size" in prediction_unit):
                                        if (not isinstance(prediction_unit["independent"], list) or
                                                not set(prediction_unit["independent"]).issubset(valid_independent_values) or
                                                not isinstance(prediction_unit["dependent"], list) or
                                                not set(prediction_unit["dependent"]).issubset(valid_dependent_values) or
                                                not isinstance(prediction_unit["test_sample_size"], Number)):
                                            raise InvalidConfigValueException("One prediction unit of "
                                                                              "the config has invalid values.")
                                    else:
                                        raise InvalidConfigKeyException("One prediction unit of the config has invalid keys.")
                                else:
                                    raise InvalidConfigValueException("One prediction unit is not of type dict")
                        else:
                            raise InvalidConfigValueException("The selected prediction option is not of type list")
            else:
                raise InvalidConfigValueException("Prediction option is not of type list")
        else:
            raise InvalidConfigKeyException("Config does not have prediction options defined.")
    else:
        raise InvalidConfigKeyException("Config does not have the field selected value.")

    if not option_found:
        raise AmbiguousConfigException("The selected value is not present in prediction options")

    return True


def check_completeness(config):
    to_be_predicted = ['freshAirIntake', 'condenser', 'evaporator', 'outlet', 'room', 'inlet']

    for entry in config:
        if 'dependent' in entry:
            curr_dependent = entry.get('dependent')
            for element in curr_dependent:
                if element in to_be_predicted:
                    to_be_predicted.remove(element)
        else:
            raise InvalidConfigKeyException('An entry of the config does not contain a dependent curve.')
    if to_be_predicted:
        raise IncompleteConfigException('In the current config not every curve is dependent')


def check_redundancies(config):
    to_be_predicted = []

    for entry in config:
        if 'dependent' in entry and "independent" in entry:
            curr_dependent = entry.get('dependent')
            curr_independent = entry.get("independent")

            if len(set(curr_dependent)) == len(curr_dependent) and len(set(curr_independent)) == len(curr_independent):
                for element in curr_dependent:
                    if element in to_be_predicted:
                        raise RedundantConfigException('Config contains redundant curves.')
                    else:
                        to_be_predicted.append(element)
            else:
                raise RedundantConfigException("Config has a dependent or independent value twice"
                                               " in the same prediction unit")
        else:
            raise InvalidConfigKeyException('An entry of the config does not contain a dependent curve.')


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
            raise InvalidConfigKeyException('An entry of the config does not contain a test sample size.')


