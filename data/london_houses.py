import numpy as np
import pandas as pd


def get_data(debug=False):
    df = pd.read_csv("data/London_houses.csv")
    df = remove_columns(df=df, columns=["no", "property_name", "postal_code"])
    df = get_categorical(
        df=df,
        columns=[
            "bedrooms",
            "bathrooms",
            "house_type",
            "receptions",
            "location",
            "city",
        ],
    )
    cat_colnames = None
    num_colnames = list(df.select_dtypes(include=[np.number]).columns.values)
    if debug:
        pass
    return df, cat_colnames, num_colnames


def remove_columns(df: pd.DataFrame, columns: list = None):
    res = df.drop(columns=columns)
    return res


def get_categorical(df: pd.DataFrame, columns: list = None):
    df[columns] = df[columns].astype("category")
    return df


if __name__ == "__main__":
    get_data(debug=True)
