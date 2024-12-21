import logging

import pandas as pd

from utils.data_manipulation import drop_outliers, get_categorical, process_null_values

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


if __name__ == "__main__":
    build_plot_df(debug=True)
