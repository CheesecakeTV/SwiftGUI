




def remove_None_vals(from_dict:dict) -> dict:
    """
    Remove all None-values from a dictionary
    :param from_dict: Will not be changed
    :return:
    """
    return dict(filter(lambda a:a[1] is not None, from_dict.items()))

