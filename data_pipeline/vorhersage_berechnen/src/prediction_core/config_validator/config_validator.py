from data_pipeline.exception.exceptions import *

import collections
import copy
from numbers import Number

valid_independent_values = ['outdoor', 'freshAirIntake', 'condenser', 'evaporator', 'outlet', 'room', 'inlet']
valid_dependent_values = ['freshAirIntake', 'condenser', 'evaporator', 'outlet', 'room', 'inlet']

mandatory_keys = ["selected_value", "prediction_options"]
top_level_keys = ["selected_value", "prediction_options"]
prediction_unit_keys = ["independent", "dependent", "test_sample_size"]


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


def has_mandatory_keys(config, keys):
    for key in keys:
        if key not in config.keys():
            raise InvalidConfigKeyException("Config does not contain mandatory field " + key + "!")


def is_instance_of(to_check, value_key, type):
    if not isinstance(to_check, type):
        raise InvalidConfigValueException(value_key + " is not of type list")


def has_valid_keys(config, valid_keys):
    if not set(config).issubset(valid_keys):
        raise InvalidConfigValueException("One prediction unit of the config has invalid values.")


def validate_preidciton_unit(prediction_option):
    is_instance_of(prediction_option, "Prediction Unit", list)
    for prediction_unit in prediction_option:
        is_instance_of(prediction_unit, "Prediction Unit", dict)
        has_mandatory_keys(prediction_unit, prediction_unit_keys)
        is_instance_of(prediction_unit["independent"], "independent list", list)
        is_instance_of(prediction_unit["dependent"], "dependent list", list)
        is_instance_of(prediction_unit["test_sample_size"], "Test sample size", Number)
        has_valid_keys(prediction_unit["independent"], valid_independent_values)
        has_valid_keys(prediction_unit["dependent"], valid_independent_values)


def check_general_constraints(config):
    has_mandatory_keys(config, top_level_keys)
    selected_value = config["selected_value"]
    prediction_options = config["prediction_options"]
    is_instance_of(prediction_options, "Prediction Options", dict)
    if selected_value not in prediction_options.keys():
        raise AmbiguousConfigException("The selected value is not present in prediction options")
    has_mandatory_keys(prediction_options, [selected_value])
    selected_prediction_unit = prediction_options[selected_value]
    validate_preidciton_unit(selected_prediction_unit)
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


