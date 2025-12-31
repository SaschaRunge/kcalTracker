import csv

class CSVLoader():
    def __init__(self, file):
        self.file = file

    def load_as_dict(self):
        data = {
            "date": [],
            "kcal": [],
            "weight": [],
        }
        with open(self.file, newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                if("date" not in row.keys() or "weight" not in row.keys() or "kcal" not in row.keys()):
                    raise Exception(f"Missing or incomplete header in '{self.file}'. Columns 'date', 'weight' and 'kcal' must exist.")
                data["date"].append(row["date"])
                data["kcal"].append(row["kcal"])
                data["weight"].append(row["weight"])
        return data
