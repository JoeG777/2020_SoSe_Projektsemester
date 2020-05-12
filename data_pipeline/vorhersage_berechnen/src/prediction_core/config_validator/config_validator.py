from data_pipeline.exception.exceptions import *

import collections
import copy
from numbers import Number

valid_independent_values = ['outdoor', 'freshAirIntake', 'condenser', 'evaporator', 'outlet', 'room', 'inlet']
valid_dependent_values = ['freshAirIntake', 'condenser', 'evaporator', 'outlet', 'room', 'inlet']

mandatory_keys = ["selected_value", "prediction_options"]
top_level_keys = ["selected_value", "prediction_options", "database_options"]
prediction_unit_keys = ["independent", "dependent", "test_sample_size"]
database_options_training_keys = ["datasource_nilan_dbname", "datasource_nilan_measurement", "datasource_weatherdata_dbname", "datasource_weatherdata_measurement"]
database_options_prediction_keys = ["datasource_forecast_dbname", "datasource_forecast_measurement", "datasource_forecast_register", "datasink_prediction_dbname", "datasink_prediction_measurement"]
database_options_mandatory_keys = ["training", "prediction"]


# TODO change single quotes to double quotes
def validate_config(config):
    """
    This method is used to validate the configuration. It checks for
    general constraints, e.g. mandatory fields,
    completeness, meaning that each necessary curve is predicted
    redundancies, e.g. restricting prediction units with the same curve defined twice in dependent
    training percentage, meaning it checks if the defined training percentages are between 0 and 1
    prediction_chain, meaning that full prediction chain can be built with the configuration

    :param config: the config to be checked
    :raises IncompleteConfigException - if every necessary curve is not defined as dependent
    :raises RedundantConfigException - if there are duplicates in one of the configs prediction unit's dependent
    or independent lists, or if there is a curve defined as dependent twice
    :raises InconsistentConfigException - if the prediction chain cannot be built with the config
    :raises InvalidTrainingPercentageException - if the training percentage is not in (0,1)
    :raises Config type exception - if the config has the wrong type
    :raises InvalidConfigKeyException - if a key in the config is invalid
    :raises InvalidConfigValueException if a value in the config is invalid
    """
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
    # implementation detail, so there is no corresponding method in documentation
    for key in keys:
        if key not in config.keys():
            raise InvalidConfigKeyException("Config does not contain mandatory field " + key + "!")


def is_instance_of(to_check, value_key, type):
    # implementation detail, so there is no corresponding method in documentation
    if not isinstance(to_check, type):
        raise InvalidConfigValueException(value_key + " is not of type " + str(type))


def has_valid_keys(config, valid_keys):
    # implementation detail, so there is no corresponding method in documentation
    if not set(config).issubset(valid_keys):
        raise InvalidConfigValueException("One prediction unit of the config has invalid values.")


def validate_prediciton_unit(prediction_option):
    # implementation detail, so there is no corresponding method in documentation
    is_instance_of(prediction_option, "Prediction Unit", list)
    for prediction_unit in prediction_option:
        is_instance_of(prediction_unit, "Prediction Unit", dict)
        has_mandatory_keys(prediction_unit, prediction_unit_keys)
        is_instance_of(prediction_unit["independent"], "independent list", list)
        is_instance_of(prediction_unit["dependent"], "dependent list", list)
        is_instance_of(prediction_unit["test_sample_size"], "Test sample size", Number)
        has_valid_keys(prediction_unit["independent"], valid_independent_values)
        has_valid_keys(prediction_unit["dependent"], valid_independent_values)


def validate_database_options(database_options):
    is_instance_of(database_options, top_level_keys[2], dict)
    if database_options_mandatory_keys[0] in database_options.keys() \
            and database_options_mandatory_keys[1] in database_options.keys():
        training = database_options.get(database_options_mandatory_keys[0])
        prediction = database_options.get(database_options_mandatory_keys[1])

        is_instance_of(training, database_options_mandatory_keys[0], dict)
        is_instance_of(prediction, database_options_mandatory_keys[1], dict)

        has_mandatory_keys(training, database_options_training_keys)
        has_mandatory_keys(prediction, database_options_prediction_keys)

        for key, value in training.items():
            is_instance_of(value, key, str)
        for key, value in prediction.items():
            is_instance_of(value, key, str)
    else:
        raise InvalidConfigKeyException("Database option of the config does not contain training/prediction")


def check_general_constraints(config):
    """
    Name in documentation: TBD
    This method checks the general structure of the config dictionary conforms to the constraints.
    E.g. if prediction options is a dictionary, e.g. if every dependent entry is a list
    :param config: The config to be checked
    """
    has_mandatory_keys(config, top_level_keys)
    validate_database_options(config["database_options"])
    selected_value = config["selected_value"]
    prediction_options = config["prediction_options"]
    is_instance_of(prediction_options, "Prediction Options", dict)
    if selected_value not in prediction_options.keys():
        raise AmbiguousConfigException("The selected value is not present in prediction options")
    has_mandatory_keys(prediction_options, [selected_value])
    selected_prediction_unit = prediction_options[selected_value]
    validate_prediciton_unit(selected_prediction_unit)


def check_completeness(config):
    """
    Name in documentation: 'vollstaendigkeit_pruefen'
    This method checks if every curve is defined as dependent once.
    :param config: The config to be checked
    :raises InvalidConfigKeyException - if a necessary key is not given(should've been checked before)
    :raises IncompleteConfigException if a necessary curve is not defined as dependent
    """
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
    """
    Name in documentation: 'redundanzen_pruefen'
    This method checks if there are no duplicates in the dependent or the independent list of a prediction unit and
    if no curve is defined as dependent twice
    :param config: the config to be checked
    :raises RedundantConfigException - in any of the cases described above
    :raises InvalidConfigKeyException - if a necessary key is not given(should've been checked before'
    """
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
    """
    Name in documentation: 'aufbau_kette_pruefen()'
    Checks if a prediction chain can be built with the config.
    :param config: the config to be checked
    :raises InconsistentConfigException - if a prediction chain can not be built with the config
    """
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
    """
    Name in documentation: 'trainings_anteil_pruefen'
    :param config: the config to be checked
    :raises InvalidTrainingPercentageException - if the training percentage is not in (0,1)
    :raises InvalidConfigKeyException - if a necessary key is not given(should've been checked before'
    """
    for entry in config:
        if 'test_sample_size' in entry:
            curr_test_sample_size = entry.get('test_sample_size')
            if curr_test_sample_size < 0 or curr_test_sample_size > 1:
                raise InvalidTrainingPercentageException('An entry of the config contains a invalid test sample size: '
                                                         + str(curr_test_sample_size))
        else:
            raise InvalidConfigKeyException('An entry of the config does not contain a test sample size.')


