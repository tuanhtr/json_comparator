
def is_json_different(target, compare_target):
    """
    Compare two object.
        If different return True, else return False
    """
    return JSONComparator.is_element_different(target, compare_target)


def is_db_data_different(expected, db_data):
    return DBComparator.is_element_different(expected, db_data)


class JSONComparator:

    @classmethod
    def is_element_different(cls, target, compare_target):
        """Compare target with compare_target"""

        # If different, return True immediately
        if type(target) != type(compare_target):
            return True
        elif type(target) == list:
            return cls.__is_list_difference(target, compare_target)
        elif type(target) == dict:
            return cls.__is_dict_difference(target, compare_target)
        elif type(target) == bool:
            return cls.__is_bool_difference(target, compare_target)
        else:
            return cls.__is_str_difference(str(target), str(compare_target))

    @classmethod
    def __is_list_difference(cls, target, compare_target):
        # If different, return True immediately
        if len(target) != len(compare_target):
            return True
        for i in range(0, len(target)):
            # If different, return True immediately
            if cls.is_element_different(target):
                return True

    @classmethod
    def __is_bool_difference(cls, target, compare_target):
        """ For boolean type """
        if target != compare_target:
            return True

    @classmethod
    def __is_str_difference(cls, target, compare_target):
        """ For string type and number type"""
        if str(target) != str(compare_target):
            return True

    @classmethod
    def __is_dict_difference(cls, target, compare_target):
        """
        Compare json
        1. Get unique keys list combine by ordered_target.keys
           and ordered_compare_target.keys
        2. Compare:
            Loop in unique_keys.
                - If key not exist in ordered_target.keys or
                 ordered_compare_target.keys --> Add to diff_key list
                - else: get value by key and compare.
        :type target: dict
        :param target:
        :type compare_target: dict
        :param compare_target:
        :rtype:
        :return:
        """
        unique_keys = cls.__get_unique_keys(target, compare_target)
        for key in unique_keys:
            if key not in target or key not in compare_target:
                return True
            if cls.is_element_different(target[key], compare_target[key]):
                return True

    @classmethod
    def __get_unique_keys(cls, *args):
        keys = []
        for arg in args:
            keys.extend(arg.keys())
        return set(keys)


class DBComparator:

    @classmethod
    def is_element_different(cls, expected, db_data, contain=True):
        """Compare target with compare_target"""
        if len(expected.keys()) > len(db_data.keys()):
            return True
        for key, value in expected.items():
            if value != db_data[key]:
                return True
