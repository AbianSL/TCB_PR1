from src.fitsanalyzer import FitsAnalyzer
from src.fitsvisualizator import FitsVisualizer
from src.csvanalyzer import CsvAnalyzer 
from src.csvvisualizator import CsvVisualizer 
from pathlib import Path
import os
from typing import List

def main():
    BASE_DIRECTORY = "./data/"
    
    # Radial Velocity
    csv = CsvAnalyzer(Path(BASE_DIRECTORY + "51_Pegasi_RVdata.csv"))
    csv.delete_outliers("err RV (m/s)", factor=1.5)
    csv.print_statistics_table()
    sis_vel = csv.get_vel()
    csv_plot = CsvVisualizer(csv)
    csv_plot.plot_rv_vs_time()
    
    
    file = FitsAnalyzer(Path(BASE_DIRECTORY + "r.HARPS.2018-09-02T03_29_21.872_S1D_A.fits"),sis_vel)
    file.print_index()
    
    ploter = FitsVisualizer(file)
    ploter.plot_spectrum()
    ploter.plot_ca_and_h_alpha()

    image = FitsAnalyzer(Path(BASE_DIRECTORY + "51_peg_hst.fits"))
    image.add_mask(Path(BASE_DIRECTORY + "star_mask.tif"),Path(BASE_DIRECTORY + "back_mask.tif"))
    imageplot = FitsVisualizer(image)
    imageplot.plot_image()
    
if __name__ == "__main__":
    main()
