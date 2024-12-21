import logging

import pandas as pd

from utils.data_manipulation import get_categorical, remove_columns

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


if __name__ == "__main__":
    build_plot_df(debug=True)
