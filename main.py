from src.manager import FitsManager
from src.visualizator import FitsVisualizer
from pathlib import Path
import os
from typing import List


def main():
    BASE_DIRECTORY = "./data/"
    directory = os.fsencode(BASE_DIRECTORY)
    
    file = FitsManager(Path(BASE_DIRECTORY + "r.HARPS.2018-09-02T03_29_21.872_S1D_A.fits"))
    ploter = FitsVisualizer(file)
    ploter.plot_spectrum()
    ploter.plot_ca_and_h_alpha()

    image = FitsManager(Path(BASE_DIRECTORY + "hst_8090_hj_wfpc2_pc_f606w_u581hj_drz.fits"))
    imageplot = FitsVisualizer(image)
    imageplot.plot_image()

    # result: List[FitsVisualizer] = []
    # for file in os.listdir(directory):
    #     file_name = os.fsdecode(file)
    #     if file_name.endswith(".fits"):
    #         path = Path(BASE_DIRECTORY + file_name)
    #         result.append(FitsManager(path))

    
    # print(f"File: {file.get_name()}")
    # for name in file.get_data().names:
    #     print(name)
    
if __name__ == "__main__":
    main()
