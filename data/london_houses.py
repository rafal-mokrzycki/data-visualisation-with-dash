import numpy as np
import pandas as pd


def get_data():
    df = pd.read_csv("data/London_houses.csv")
    df = remove_columns(df=df, columns=["no", "property_name", "postal_code"])
    cat_colnames = None
    num_colnames = list(df.select_dtypes(include=[np.number]).columns.values)
    return df, cat_colnames, num_colnames


def remove_columns(df: pd.DataFrame, columns: list = None):
    result = df.drop(columns=columns)
    return result


if __name__ == "__main__":
    get_data()
