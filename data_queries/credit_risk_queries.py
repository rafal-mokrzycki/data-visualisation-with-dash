import logging

import numpy as np
import pandas as pd
from scipy import stats

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)


def build_plot_df(debug=False):
    df = pd.read_csv("data/raw_data/credit_risk_dataset.csv")
    cat_columns = [
        "person_home_ownership",
        "loan_intent",
        "loan_grade",
        "loan_amnt",
        "loan_status",
        "cb_person_default_on_file",
    ]
    df = get_categorical(
        df=df,
        columns=cat_columns,
    )
    df = process_null_values(df)
    df = drop_outliers(df=df, columns=["person_age"])

    if debug:
        logging.debug(f"DATAFRAME:\n{df.head()}")
        logging.debug(f"DATATYPES:\n{df.dtypes}")
        logging.debug(f"DATAFRAME (more info):\n{df.describe()}")
        logging.debug(f"DATAFRAME (null values):\n{df.isna().sum()}")
    return df, cat_columns


def get_categorical(df: pd.DataFrame, columns: list = None):
    df[columns] = df[columns].astype("category")
    return df


def process_null_values(df: pd.DataFrame):
    res = df.dropna()
    return res


def drop_outliers(df: pd.DataFrame, threshold: int = 3, columns: list = None):
    # Calculate Z-scores
    z_scores = np.abs(stats.zscore(df[columns]))

    # Create a boolean mask for rows that are not outliers
    mask = (z_scores < threshold).all(axis=1)

    # Filter the DataFrame to remove outliers
    return df[mask]


if __name__ == "__main__":
    build_plot_df(debug=True)
