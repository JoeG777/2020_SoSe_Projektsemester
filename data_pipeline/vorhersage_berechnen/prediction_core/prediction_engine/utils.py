ALL_CURVES = ["freshAirIntake", "inlet", "room", "outlet", "condenser", "evaporator"]
PREDICTION_BASIS = {
    "outdoor": "check"
}


def intersection(lst1, lst2):
    # Returns the intersection of two lists.
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def is_subset(list1, list2):
    # Checks if the first list is a subset of the second list.
    a = len(intersection(list1, list2))
    b = len(list1)
    return len(intersection(list1, list2)) == len(list1)


def copy_from_dict_to_dict(dict1, dict2):
    # Copies a dictionaries keys and values to another dictionary.
    for key in dict1.keys():
        dict2[key] = dict1[key]


def verify_config(config):
    # Verifies the config given as a parameter. A config is verified when all Strings defined in ALL_CURVES are
    # present and all independent values can be build.
    if not has_all_curves(config):
        return False
    return check_build_chain(config)


def has_all_curves(config):
    # Checks if all curves are defined in a list of config elements.
    for curve in ALL_CURVES:
        has_element = False
        for element in config:
            if has_element:
                continue
            as_list = [curve]
            if is_subset(as_list, element["dependent"]):
                has_element = True
        if not has_element:
            return False
    return True


# Checks if all necessary independent parameters can be build.
def check_build_chain(config):
    config_data = config.copy()
    known_data_sources = PREDICTION_BASIS.copy()
    entry_removed = True
    while len(config_data) > 0:
        if not entry_removed:
            return False
        entry_removed = False
        for config in config_data:
            config_indep = config.get("independent")
            config_dep = config.get("dependent")
            if is_subset(config_indep, known_data_sources.keys()):
                config_data.remove(config)
                known_data_sources[config_dep] = "check"
                entry_removed = True
    return True
