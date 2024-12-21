import pandas as pd

from utils.data_manipulation import drop_outliers, get_categorical, process_null_values
from utils.logging import logger


def build_plot_df(debug: bool = False) -> tuple[pd.DataFrame, list]:
    """
    Load and prepare the credit risk dataset for plotting.

    Parameters:
    debug (bool): If True, enables debug logging to provide insights into
                  the loaded DataFrame, including its head, data types,
                  summary statistics, and null value counts.

    Returns:
    tuple[pd.DataFrame, list]: A tuple containing the DataFrame with
                                processed data and a list of categorical
                                columns.
    """
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
        logger.debug(f"DATAFRAME:\n{df.head()}")
        logger.debug(f"DATATYPES:\n{df.dtypes}")
        logger.debug(f"DATAFRAME (more info):\n{df.describe()}")
        logger.debug(f"DATAFRAME (null values):\n{df.isna().sum()}")
    return df, cat_columns


if __name__ == "__main__":
    build_plot_df(debug=True)
