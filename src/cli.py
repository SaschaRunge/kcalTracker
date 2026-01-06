import sys
from csv_writer import CSVWriter

PATH_TO_FILE = "./data/generated/output.csv"

class CLI():
    def __init__(self, dataset):
        self.dataset = dataset

        self.valid_input = {"quit": ["quit", "q"],
                            "show": ["show", "s"],
                            "write": ["write", "w"]}

        print("")
        print(f"{' kCalc ':=^50}")
        print("")
        
    def run(self):
        while True:
            cmd = input("> ")
            if cmd in self.valid_input["quit"]:
                sys.exit(0)
            if cmd in self.valid_input["show"]:
                self._show()
            if cmd in self.valid_input["write"]:
                self._write(PATH_TO_FILE)

    def _show(self):
        width = {"date": 14,
                "weight": 8,
                "kcal": 10,
                "default": 10}
        
        line = "|"
        for key in self.dataset:
            if key in width:
                line += f"{key:^{width[key]}}|"
            else:
                line += f"{key:^{width["default"]}}|"
        print(line)
        print(f"{'':=^{len(line)}}")

        for i in range(len(self.dataset["date"])):
            line = "|"
            for key, values in self.dataset.items():
                if key in width:
                    line += f"{str(values[i]):^{width[key]}}|"
                else:
                    line += f"{str(values[i]):^{width["default"]}}|"
            print(line)
    
    def _write(self, file):
        print(f"Writing to file '{file}... .")
        try:
            writer = CSVWriter(file)
            writer.write(self.dataset)
            print(f"Successful.")
        #TODO: evaluate type of error
        except Exception as e:
            print(f"Could not write to file: {e}")



            
            


