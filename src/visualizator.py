from astropy.table import Table 
from .manager import FitsManager
from .utils import calculate_data_masked_vim_vmax
import matplotlib.pyplot as plt

class FitsVisualizer:

    def __init__(self, manager: FitsManager) -> None:
        self._manager = manager
        self._output_folder = "outputs/"

    def plot_image(self) -> None:
        data = self._manager.get_data()
        data_masked, vmin, vmax = calculate_data_masked_vim_vmax(data)
        plt.figure(figsize=(10, 10))
        plt.imshow(data_masked, cmap="gray", vmin=vmin, vmax=vmax) 
        plt.colorbar()
        plt.title("Image from fits file")
        self._save_fig("image") 

    def plot_spectrum(self) -> None:
        self._only_plot_spectrum()
        plt.title("51 pegasi")
        self._save_fig("espectro")
    
    def plot_ca_and_h_alpha(self) -> None:
        ca_h_min = 3920
        ca_h_max = 3980
        h_alpha_min = 6540
        h_alpha_max = 6590

        self._only_plot_spectrum()
        plt.subplot(1, 1, 1)
        plt.xlim(ca_h_min, ca_h_max)
        plt.title("Espectro enfocando a Ca H")

        self._only_plot_spectrum()
        plt.subplot(1, 2, 2)
        plt.xlim(h_alpha_min, h_alpha_max)
        plt.title("Espectro enfocando a H alpha")
        self._save_fig("zoom")

        plt.clf()

    def _only_plot_spectrum(self) -> None:
        wave = self._manager.get_wavelength()
        flux = self._manager.get_flux()
        plt.figure(figsize=(10, 10))
        plt.yscale("log")
        plt.plot(wave, flux)
        plt.xlabel("Wavelength")
        plt.ylabel("Flux")

    def _save_fig(self, name: str, extension: str = ".png") -> None:
        if name.endswith(".png"):
            extension = ""
        plt.savefig(self._output_folder + name + extension, dpi=300, bbox_inches="tight")
