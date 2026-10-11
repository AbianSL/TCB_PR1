from astropy.table import Table 
from .fitsanalyzer import FitsAnalyzer
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from astropy.wcs import WCS

class FitsVisualizer:
    """
    A class to visualize data from a FITS file managed by FitsAnalyzer.
    """

    # Global plotting defaults
    plot_params = {
        "figure.figsize": (3.4, 3.4),
        "figure.dpi": 1200,
        "axes.titlesize": 8,
        "axes.labelsize": 8,
        "axes.linewidth": .5,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "lines.linewidth": .5,
        "lines.markersize": 5,
        "legend.fontsize": 8,
        }
    plt.rcParams.update(plot_params)
    
    def __init__(self, manager: FitsAnalyzer) -> None:
        self._manager = manager
        self._output_folder = "outputs/"

    def plot_image(self) -> None:
        data = self._manager.get_data()
        data1 = np.ma.masked_invalid(data)        
        hdr=self._manager._header
        wcs = WCS(hdr)
        
        photflam = hdr['PHOTFLAM']
        photplam = hdr['PHOTPLAM']
        
        # Pixel area in arcsec^2
        pixscale = abs(hdr['CD1_1']) * 3600  # arcsec/pixel
        pixarea = pixscale**2
        
        texp = hdr['EXPTIME']
        intensity = data1 / texp * photflam / pixarea
        
        data1 = np.full(data1.shape, np.nan)
        valid = intensity > 0
        
        # Convert erg/s/cm^2/armstrong/arcsec^2 to mag/arcsec^2
        data1[valid] = ( -2.5 * np.log10(intensity[valid]) - 5 * np.log10(photplam) - 2.406)           
        mask = self._manager._mask[0] + self._manager._mask[1]
        data2 = np.ma.masked_where(mask == 0, intensity)
        
        fig1, ax1 = plt.subplots(subplot_kw={'projection': wcs})
        fig2, ax2 = plt.subplots(subplot_kw={'projection': wcs})        
        
        im1=ax1.imshow(data1, cmap="plasma_r", vmin=23, vmax=30)
        im2=ax2.imshow(data2, cmap="Greys_r"  , vmin=-2e-19,vmax=1e-18)
        
        for im,fig,ax in zip((im2,im1),(fig2,fig1),(ax2,ax1)):
            cbar=fig1.colorbar(im, ax=ax)
            ax.set_xlim(0,3750)
        cbar.ax.invert_yaxis()
        cbar.set_label(r'$\mu_{\rm AB}$ (mag arcsec$^{-2}$)')

        ax1.set_title("Image from fits file")
        self._save_fig("image",fig1) 
        ax2.set_title("Image from fits file")
        self._save_fig("image2",fig2) 

    def plot_spectrum(self) -> None:
        self._only_plot_spectrum()
        plt.title("51 pegasi")
        self._save_fig("espectro")
        
    def _only_plot_spectrum(self) -> None:
        """
        Plot the spectrum of the data managed by FitsAnalyzer.
        """
        wave = self._manager.get_wavelength()
        flux = self._manager.get_flux()
        plt.figure(figsize=(10, 10))
        plt.yscale("log")
        plt.plot(wave, flux)
        plt.xlabel("Wavelength")
        plt.ylabel("Flux")
        
    def plot_ca_and_h_alpha(self) -> None:
        wave = self._manager.get_wavelength()
        flux = self._manager.get_flux()
        fig1, axes1 = plt.subplots(2, 2)
        fig2, axes2 = plt.subplots(1, 1, figsize=(3.4,1.6))
        
        axes={"caii_k": axes1[0,0],
              "caii_h": axes1[0,1],
              "r"     : axes1[1,0],
              "v"     : axes1[1,1],
              "ha"    : axes2,
              "alpha_c": axes2,
              "alpha_l": axes2,
              "alpha_r": axes2}

        # move axes of right figures to the right
        for i in (0,1):
            axes1[i,1].yaxis.tick_right()
            axes1[i,1].yaxis.set_label_position("right")
        
        # spectra and y-ax tick
        for ax in axes.values():
            # same data for all subplots
            ax.plot(wave, flux, color='black', zorder=10)     
            # scientific format for y-ax tick's labels
            ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0), useMathText=True)
        
        left, right, max_flux = {}, {}, {}
                   
        for band in ("caii_k","caii_h"):
            left[band] = self._manager.get_centre(band) - self._manager.get_fwhm(band) * 1.5
            right[band] = self._manager.get_centre(band) + self._manager.get_fwhm(band) * 1.5
            max_flux [band]= np.max(flux[(wave >= left[band]) & (wave <= right[band])])
            
            x0 = self._manager.get_centre(band)
            fwhm = self._manager.get_fwhm(band)
            ymax = max_flux[band]
            
            axes[band].axvline(x=x0, color="red", linestyle="--")
            axes[band].fill([x0-fwhm, x0, x0+fwhm], [0, ymax, 0],
                            color="red", edgecolor=None, alpha=0.2)
        
        for band in ("r","v"):
            left[band] = self._manager.get_centre(band) - self._manager.get_fwhm(band) * 1.5 / 2
            right[band] = self._manager.get_centre(band) + self._manager.get_fwhm(band) * 1.5 / 2
            max_flux[band] = np.max(flux[(wave >= left[band]) & (wave <= right[band])])
        
        left ["ha"] = self._manager.get_centre("alpha_l") - self._manager.get_fwhm("alpha_l") * 1.5 / 2
        right["ha"] = self._manager.get_centre("alpha_r") + self._manager.get_fwhm("alpha_r") * 1.5 / 2
        max_flux["ha"] = np.max(flux[(wave >= left["ha"]) & (wave <= right["ha"])])

        for band in ("r","v","alpha_c","alpha_l","alpha_r"):
            x0 = self._manager.get_centre(band)
            width = self._manager.get_fwhm(band)
            axes[band].axvspan(x0 - width/2, x0 + width/2, 
                               color="red", linewidth=0, alpha=0.2)     

        for band in ("caii_k","caii_h","r","v","ha"):
            axes[band].set_xlim(left[band],right[band])
            axes[band].set_ylim(0,max_flux[band]*1.2)

        fig1.tight_layout()
        self._save_fig("zoom2",fig1)
        plt.figure(fig1.number)
        plt.show()   
        
        fig2.tight_layout()
        self._save_fig("zoom3",fig2)
        plt.figure(fig2.number)
        plt.show()
       
    def _save_fig(self, name: str, fig=None, extension: str = ".png") -> None:
        """
        Save the current figure or a specified figure to the output folder with the given name and extension.º
        """
        if name.endswith(".png"):
            extension = ""
        if fig:
            fig.savefig(self._output_folder + name + extension,
                        dpi=1200, bbox_inches="tight")
        else:
            plt.savefig(self._output_folder + name + extension,
                        dpi=300, bbox_inches="tight")
