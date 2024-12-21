import logging

import pandas as pd

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)


def build_plot_df(debug=False):
    df = pd.read_csv("data/raw_data/London_houses.csv")
    cat_columns = [
        "bedrooms",
        "bathrooms",
        "house_type",
        "receptions",
        "location",
        "city",
    ]
    df = remove_columns(df=df, columns=["no", "property_name", "postal_code"])
    df = get_categorical(
        df=df,
        columns=cat_columns,
    )
    if debug:
        logging.debug(f"DATAFRAME:\n{df.head()}")
        logging.debug(f"DATATYPES:\n{df.dtypes}")
        logging.debug(f"DATAFRAME (more info):\n{df.describe()}")
        logging.debug(f"DATAFRAME (null values):\n{df.isna().sum()}")
    return df, cat_columns


def remove_columns(df: pd.DataFrame, columns: list = None):
    res = df.drop(columns=columns)
    return res


def get_categorical(df: pd.DataFrame, columns: list = None):
    df[columns] = df[columns].astype("category")
    return df


if __name__ == "__main__":
    build_plot_df(debug=True)