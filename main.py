from src.manager import FitsManager
from src.visualizator import FitsVisualizer
from src.csvanalyzer import CsvAnalyzer 
from src.csvvisualizator import CsvVisualizer 
from pathlib import Path
import os
from typing import List


def main():
    BASE_DIRECTORY = "./data/"
    
    # file = FitsManager(Path(BASE_DIRECTORY + "r.HARPS.2018-09-02T03_29_21.872_S1D_A.fits"))
    # ploter = FitsVisualizer(file)
    # ploter.plot_spectrum()
    # ploter.plot_ca_and_h_alpha()

    # image = FitsManager(Path(BASE_DIRECTORY + "hst_8090_hj_wfpc2_pc_f606w_u581hj_drz.fits"))
    # imageplot = FitsVisualizer(image)
    # imageplot.plot_image()
    
    csv = CsvAnalyzer(Path(BASE_DIRECTORY + "51_Pegasi_RVdata.csv"))
    csv.delete_outliers("err RV (m/s)", factor=1.5)
    # csv.print_statistics_table()

    csv_plot = CsvVisualizer(csv)
    csv_plot.plot_rv_vs_time()
    

if __name__ == "__main__":
    main()
