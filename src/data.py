import os
import sys
import csv
import datetime

from enum import Enum
from parser import Parser

PATH_TO_FILE = "./data/input/input.csv"

class DataType(Enum):
    INTEGER = 0
    FLOAT = 1
    DATE = 2

class InvalidTypeException(Exception):
    pass

class Data():
    def __init__(self, filename = PATH_TO_FILE):
        self.source_data = {
            "date": [],
            "kcal": [],
            "weight": [],
        }
        self.generated_data = {}

        self._import_data_as_dict(filename)
        self._normalize_all_inputs()
    
    def _import_data_as_dict(self, filename):
        #TODO: abspath to csv
        
        try:
            with open(filename, newline='') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                for row in csv_reader:
                    if("date" not in row.keys() or "weight" not in row.keys() or "kcal" not in row.keys()):
                        raise Exception(f"Missing or incomplete header in '{filename}'. Columns 'date', 'weight' and 'kcal' must exist.")
                    self.source_data["date"].append(row["date"])
                    self.source_data["kcal"].append(row["kcal"])
                    self.source_data["weight"].append(row["weight"])
        except Exception as e:
            sys.exit(f"Error: Unable to read data from '{filename}':\n{e}")

        if(self._has_duplicates(self.source_data["date"])):
            sys.exit(f"Error: Duplicate entries in column 'date' in '{filename}' are invalid. Exiting... .")

        #TODO: maybe handle missing values differently. This might make it a bit annoying to add single values to a dataset, might need to remove lines with empty values for calculation instead
        if (self._has_empty_values(self.source_data["date"]) or
            self._has_empty_values(self.source_data["kcal"]) or
            self._has_empty_values(self.source_data["weight"])):
            sys.exit(f"Error: Dataset '{filename}' has missing values. Exiting... .")
    
    def _has_duplicates(self, data):
        unique_values = set()

        for value in data:
            if value in unique_values:
                return True
            unique_values.add(value)       
        return False

    def _has_empty_values(self, data):
        for value in data:
            if not value:
                return True
        return False

    def _normalize_input(self, strings, datatype):
        normalized_input = []
        try:
            for string in strings:
                match(datatype):
                    case DataType.INTEGER:
                        value = Parser.parse_int(string)
                    case DataType.FLOAT:
                        value = Parser.parse_float(string)
                    case DataType.DATE:
                        value = Parser.parse_date(string)
                    case _:
                        raise InvalidTypeException(f"Invalid datatype {datatype} in {os.path.abspath(__file__)} in {self._normalize_input.__name__}.")
                normalized_input.append(value)
        except ValueError as e:
            sys.exit(f"ValueError: Could not convert string to datatype {datatype} (likely due to invalid formatting of your .csv): {e}") 

        return normalized_input

    def _normalize_all_inputs(self):
        self.generated_data["date"] = self._normalize_input(self.source_data["date"], DataType.DATE)
        self.generated_data["kcal"] = self._normalize_input(self.source_data["kcal"], DataType.FLOAT)
        self.generated_data["weight"] = self._normalize_input(self.source_data["weight"], DataType.FLOAT)

    def add(self, data, key):
        for _, v in self.generated_data.items():
            if len(v) != len(data):
                raise NotImplementedError("TODO: Make sure to enforce consistent length for all lists stored in generated data (class Data).")
        self.generated_data[key] = data

    ### Returns the specified data in column key between two dates. If the end date is earlier than the start date, end date is set to start date. ###
    def get_by_date(self, key, date_start, date_end=None):
        dates = self.generated_data["date"]

        if key not in self.generated_data.keys():
            return None
        if not dates:
            return []
        
        if not isinstance(date_start, datetime.date):
            date_start = Parser.parse_date(date_start)
        if date_end is None:
            date_end = date_start
        elif not isinstance(date_end, datetime.date):
            date_end = Parser.parse_date(date_end)

        if date_end < date_start:
            date_end = date_start

        i = 0
        while (i < len(dates) and date_start > dates[i]):
            i += 1
        if i < len(dates) and date_start >= dates[i]:
            lower_index = i
        else:
            return []
        while (i < len(dates) and date_end > dates[i]):
            i += 1
        if i < len(dates):
            upper_index = i
        else:
            upper_index = len(dates) - 1

        return  self.generated_data[key][lower_index:upper_index + 1]

if __name__ == '__main__':
    Data()