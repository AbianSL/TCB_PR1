import csv

class CSVManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.read_csv()

    def read_csv(self):
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]

    def get_data(self):
        return self.data

    def get_column(self, column_name):
        return [row[column_name] for row in self.data if column_name in row]
