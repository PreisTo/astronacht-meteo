import numba as nb
import numpy as np


@nb.njit
def angular_distance_fast_rad(lon1: float, lat1: float, lon2: float, lat2: float):
    """Compute angular distance using the Haversine formula. For angles in rad!

    :param lon1: position 1 longitude in rad
    :type lon1: float
    :param lat1: position 1 latitude in rad
    :type lat1: float
    :param lon2: position 2 longitude in rad
    :type lon2: float
    :param lat2: position 2 latitude in rad
    :type lat2: float

    :return angular distance in rad:
    :rtype float:
    """
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    return 2 * np.arcsin(np.sqrt(a))
