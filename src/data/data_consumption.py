import pandas as pd


def obtain_file_as_dataframe(file: str, directory: str = "data", delimiter: str = ","):
    df = pd.read_csv(directory + "/" + file, sep=delimiter)
    return df
