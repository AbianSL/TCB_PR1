from astropy.table import Table 
from .utils import calculate_data_masked_vim_vmax
import matplotlib.pyplot as plt


class CsvVisualizer:
    """
    A class to visualize data from a CSV file managed by CsvAnalyzer.
    """

    def __init__(self, manager: DataFrame) -> None:
        self._manager = manager
        self._output_folder = "outputs/"
    
    def plot_rv_vs_time(self) -> None:
        """
        Plots RV (m/s) vs Time (JD) with error bars.
        """
        df = self._manager.get_dataframe_with_offsets()
        instruments = df["Inst"].unique()
        
        plt.figure(figsize=(10, 6))
        colors = plt.cm.tab10.colors
        markers = ["o", "s", "^", "v", "D", "P", "X", "<", ">", "*"]

        for idx, instrument in enumerate(instruments):
            instrument_data = df[df["Inst"] == instrument]
            marker = markers[idx % len(markers)]
            color = colors[idx % len(colors)]

            plt.errorbar(instrument_data["BJD"], 
                         instrument_data["RV (m/s)"], 
                         yerr=instrument_data["err RV (m/s)"], 
                         fmt=marker,
                         color=color,
                         label=f'Instrument: {instrument}', 
                         alpha=0.7)
        
        plt.title("Radial Velocity vs Time")
        plt.xlabel("Time (JD)")
        plt.ylabel("Radial Velocity (m/s)")
        plt.grid(True)
        plt.legend()
        self._save_fig("rv_vs_time")

    def _save_fig(self, name: str, extension: str = ".png") -> None:
        if name.endswith(".png"):
            extension = ""
        plt.savefig(self._output_folder + name + extension, dpi=300, bbox_inches="tight")
