import pandas as pd

from utils.data_manipulation import get_categorical, remove_columns
from utils.logging import logger


def build_plot_df(debug: bool = False) -> tuple[pd.DataFrame, list]:
    """
    Load and prepare the housing dataset for plotting.

    Parameters:
    debug (bool): If True, enables debug logging to provide insights into
                  the loaded DataFrame, including its head, data types,
                  summary statistics, and null value counts.

    Returns:
    tuple[pd.DataFrame, list]: A tuple containing the DataFrame with
                                processed data and a list of categorical
                                columns.
    """

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
        logger.debug(f"DATAFRAME:\n{df.head()}")
        logger.debug(f"DATATYPES:\n{df.dtypes}")
        logger.debug(f"DATAFRAME (more info):\n{df.describe()}")
        logger.debug(f"DATAFRAME (null values):\n{df.isna().sum()}")
    return df, cat_columns


if __name__ == "__main__":
    build_plot_df(debug=True)
