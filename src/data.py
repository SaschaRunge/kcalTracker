import os
import datetime

from csv_loader import CSVLoader

from enum import Enum
from parser import Parser

PATH_TO_FILE = "./data/input/input.csv"

class DataType(Enum):
    INTEGER = 0
    FLOAT = 1
    DATE = 2

class InvalidTypeException(Exception):
    pass
class InvalidInputException(Exception):
    pass

class Data():
    def __init__(self, filename = PATH_TO_FILE):
        self.source_data = {}       # raw input
        self.data = {}              # complete, normalized dataset

        self._import_from_csv(filename)
        self._normalize_data()
    
    def _import_from_csv(self, filename):
        csv_loader = CSVLoader(filename)
        self.source_data = csv_loader.load_as_dict()
        
        if(self._has_duplicates(self.source_data["date"])):
            raise InvalidInputException(f"Error: Duplicate entries in column 'date' in '{filename}' are invalid.")

        #TODO: maybe handle missing values differently. This might make it a bit annoying to add single values to a dataset, might need to remove lines with empty values for calculation instead
        if (self._has_empty_values(self.source_data["date"]) or
            self._has_empty_values(self.source_data["kcal"]) or
            self._has_empty_values(self.source_data["weight"])):
            raise InvalidInputException(f"Error: Dataset '{filename}' has missing values.")
    
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

    def _normalize(self, strings, datatype):
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
                        raise InvalidTypeException(f"Invalid datatype {datatype!r}.")
                normalized_input.append(value)
        except ValueError as e:
            raise InvalidInputException(f"InvalidInputException: Could not convert string to datatype {datatype!r} (likely due to invalid formatting of your .csv): {e}") 

        return normalized_input

    def _normalize_data(self):
        self.data["date"] = self._normalize(self.source_data["date"], DataType.DATE)
        self.data["kcal"] = self._normalize(self.source_data["kcal"], DataType.FLOAT)
        self.data["weight"] = self._normalize(self.source_data["weight"], DataType.FLOAT)

    def add(self, data, key):
        for _, v in self.data.items():
            if len(v) != len(data):
                raise NotImplementedError("TODO: Make sure to enforce consistent length for all lists stored in generated data (class Data).")
        self.data[key] = data

    ### Returns the specified data in column key between two dates. If the end date is earlier than the start date, end date is set to start date. ###
    def get_by_date(self, key, date_start, date_end=None):
        dates = self.data["date"]

        if key not in self.data:
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

        return  self.data[key][lower_index:upper_index + 1]

if __name__ == '__main__':
    Data()