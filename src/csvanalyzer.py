import pandas as pd

class CsvAnalyzer:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.read_csv() 

    def read_csv(self):
        """
        Reads the CSV file and stores it in a DataFrame.
        """
        try:
            self.dataframe = pd.read_csv(self.file_path)
        except Exception as error:
            print(f"Error reading CSV file: {error}")

    def get_dataframe(self):
        """
        Returns the DataFrame.
        """
        return self.dataframe

    def get_column(self, column_name):
        """
        Returns a specific column from the DataFrame.
        """
        if column_name in self.dataframe.columns:
            return self.dataframe[column_name]
        else:
            print(f"Column '{column_name}' does not exist in the DataFrame.")
            return None
    
    def delete_outliers(self, column_name: str, factor: float = 1.5) -> None:
        """
        Removes rows where the specified column value falls outside the IQR bounds.
        
        Keeps values satisfying:
            Q1 - factor * IQR <= value <= Q3 + factor * IQR
        """
        if column_name not in self.dataframe.columns:
            raise KeyError(f"Column '{column_name}' does not exist in the DataFrame.")

        self.dataframe[column_name] = pd.to_numeric(self.dataframe[column_name], errors="coerce")

        q1 = self.dataframe[column_name].quantile(0.25)
        q3 = self.dataframe[column_name].quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - factor * iqr
        upper_bound = q3 + factor * iqr

        initial_count = len(self.dataframe)

        valid_mask = (self.dataframe[column_name] >= lower_bound) & (
            self.dataframe[column_name] <= upper_bound
        )
        self.dataframe = self.dataframe[valid_mask].reset_index(drop=True)

    def calculate_statistics(self) -> Dict[str, Tuple]:
        """
        Calculates and returns basic statistics (mean, std, error mean) per instrument.
        """
        instruments = self.dataframe["Inst"].unique()
        results = {}
        for instrument in instruments:
            instrument_data = self.dataframe[self.dataframe["Inst"] == instrument]
            mean = instrument_data["RV (m/s)"].mean()
            std = instrument_data["RV (m/s)"].std()
            error_mean = instrument_data["err RV (m/s)"].mean()
            results[instrument] = (mean, std, error_mean)
        return results
    
    def get_dataframe_with_offsets(self) -> pd.DataFrame:
        """
        Returns a new DataFrame with the offsets for each instrument fixed.
        """
        df = self.dataframe.copy()
        instruments = df["Inst"].unique()
        for instrument in instruments:
            instrument_data = df[df["Inst"] == instrument]
            mean_rv = instrument_data["RV (m/s)"].mean()
            df.loc[df["Inst"] == instrument, "RV (m/s)"] -= mean_rv
        return df

    def print_statistics_table(self) -> None:
        """
        Prints a neatly formatted table in console.
        Reuses precomputed statistics if provided; computes them otherwise.
        """
        stats = self.calculate_statistics()

        col_inst = "Instrument"
        col_mean = "Mean RV (m/s)"
        col_std = "Std RV (m/s)"
        col_err = "Mean Err (m/s)"

        header = f"{col_inst:<12} | {col_mean:>15} | {col_std:>14} | {col_err:>14}"
        separator = "-" * len(header)

        print("\n" + separator)
        print(header)
        print(separator)

        for inst, (mean_val, std_val, err_val) in stats.items():
            print(f"{inst:<12} | {mean_val:>15.3f} | {std_val:>14.3f} | {err_val:>14.3f}")

        print(separator + "\n")
