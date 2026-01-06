from dataset import DataSet
from math_m import Math_m
from cli import CLI

def main():
    dataset = DataSet()
    cli = CLI(dataset.get())
    cli.run()

if __name__ == '__main__':
    main()