from astropy.io import fits
from astropy.table import Table 
from pathlib import Path
import numpy as np
from typing import List
from PIL import Image
import matplotlib.pyplot as plt

class FitsAnalyzer:
    """
    Class to store the fists important data
    """
    
    def __init__(self, file_name: Path, vel: float = None) -> None:
        """
        Constructor of the class.
            file_name: The location of the file 
        """
        try:
            with fits.open(file_name) as hdul:
                self._hdul = hdul.copy()
                self._data = hdul[1].data
                self._header=hdul[0].header
                self._header.extend(hdul[1].header, update=True)
                self._table = Table(self._data)
                self._name = file_name.name
                if isinstance(hdul[1], (fits.BinTableHDU, fits.TableHDU)):
                    self.__mask = self._data["quality"] == 0
        except EOFError or FileNotFoundError as error:
            print(f"code {error.errno}: {error.strerror}")
        except Exception as error:
            print(f"Unkown error: {error}")
        
        if vel is not None:
            self._vel = vel

        # In Amstrongs
        self._bands = {
            "caii_h": (3968.470, 1.09),
            "caii_k": (3933.664, 1.09),
            "r":      (4001.070, 20.0),
            "v":      (3901.070, 20.0),
            "alpha_c": (6562.808, 1.60),
            "alpha_l": (6550.870, 10.75),
            "alpha_r": (6580.310, 8.75),
            }
        
    def print_info(self) -> None:
        self._hdul.info()
    
    def get_flux(self) -> np.ndarray:
        """
        Get the flux data from the FITS file, applying a quality mask to filter out bad data points.
        """
        return self._data["flux"][self.__mask]

    def get_wavelength(self) -> np.ndarray:
        """
        Get the wavelength data from the FITS file, applying a quality mask to filter out bad data points. If the wavelength has not been calculated yet, it will be computed using the `calc_wave` method.
        """
        if not hasattr(self, "wave"):
            self.calc_wave()        
        return self._wave

    def calc_wave(self) -> None:
        """
        Calculate the wavelength in vacuum from the wavelength in air, applying a Doppler shift based on the radial velocity. The result is stored in the `_wave` attribute.
        """
        wave_air = self._data["wavelength_air"][self.__mask]
        c = 299792458 # Speed of light in m/s
        self._wave = wave_air / (1 + self._vel / c)
    
    def get_table(self) -> Table:
        return self._table

    def get_header(self, value: int = 0) -> fits.Header:
        return self._hdul[value].header
   
    def get_data(self) -> np.ndarray:
        return self._data

    def get_name(self) -> str:
        return self._name
    
    def print_index(self) -> None:
        wave=self.get_wavelength()
        flux=self.get_flux()
              
        band_flux={}
        trapz_func = getattr(np, "trapezoid", getattr(np, "trapz", None))
        
        for band in ("caii_h", "caii_k"):
            centre, fwhm = self._bands[band]
            weigth = np.maximum(0, 1 - np.abs(wave - centre) / fwhm)
            band_flux[band] = trapz_func(flux * weigth, wave)
        
        for band in ("r", "v", "alpha_c", "alpha_l", "alpha_r"):
            centre, fwhm = self._bands[band]
            mask = abs(wave - centre) < fwhm / 2           
            band_flux[band] = trapz_func(flux[mask], wave[mask])
        
        s_index = 2.3 * 8 * (band_flux["caii_h"] + band_flux["caii_k"]) / (band_flux["r"] + band_flux["v"])
        ha_index = band_flux["alpha_c"] / (band_flux["alpha_l"] + band_flux["alpha_r"])
        
        print( "S index: ", s_index)
        print("Ha index: ", ha_index)
    
    def add_mask(self, *args) -> None:
        """
        Add multiple masks to the FitsAnalyzer instance. Each mask is created from an image file, where pixel values greater than 127 are considered part of the mask (set to 1), and others are set to 0.
        """
        self._mask = []
        for path in args:
            data = np.array(Image.open(path))
            data = (data > 127).astype(np.uint8)
            self._mask.append(data)         
