import pandas as pd


def get_data():
    df = pd.read_csv("data/London_houses.csv")
    return df


def remove_columns(df: pd.DataFrame, cols: list = None):
    return df


if __name__ == "__main__":
    get_data()
