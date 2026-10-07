from astropy.io import fits
from astropy.table import Table 
from pathlib import Path
import numpy as np
from typing import List

class FitsManager:
    """
    Class to store the fists important data
    """
    
    def __init__(self, file_name: Path) -> None:
        """
        Constructor of the class.
            file_name: The location of the file 
        """
        try:
            with fits.open(file_name) as hdul:
                self._hdul = hdul.copy()
                self._data = hdul[1].data
                self._table = Table(self._data)
                self._name = file_name.name
                if isinstance(hdul[1], (fits.BinTableHDU, fits.TableHDU)):
                    self.__mask = self._data["quality"] == 0
        except EOFError or FileNotFoundError as error:
            print(f"code {error.errno}: {error.strerror}")
        except Exception as error:
            print(f"Unkown error: {error}")
    

    def print_info(self) -> None:
        """
        Print the info from the file
        """
        self._hdul.info()
    
    def get_flux(self):
        return self._data["flux"][self.__mask]

    def get_wavelength(self):
        return self._data["wavelength_air"][self.__mask]
    
    def get_table(self) -> Table:
        return self._table

    def get_header(self, value: int = 0) -> Header:
        return self._hdul[value].header
   
    def get_data(self):
        return self._data

    def get_name(self) -> str:
        return self._name
