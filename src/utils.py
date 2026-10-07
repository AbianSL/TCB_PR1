import numpy as np
from astropy.io import fits

def calculate_data_masked_vim_vmax(data) -> tuple:
    """
    Get the minimum and maximum values of the data
    """
    new_data = np.asarray(data, dtype=np.float64)
    valid = np.isfinite(data)
    data_masked = np.ma.masked_invalid(new_data)
    vmin, vmax = np.percentile(data[valid], [5, 95])
    return (data_masked, vmin, vmax)
