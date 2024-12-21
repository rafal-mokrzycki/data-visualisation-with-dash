import numpy as np
import pandas as pd
from scipy import stats


def get_categorical(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """
    Convert specified columns in a DataFrame to categorical type.

    Parameters:
    df (pd.DataFrame): The DataFrame to modify.
    columns (list): A list of column names to convert to categorical.

    Returns:
    pd.DataFrame: The modified DataFrame with specified columns as categorical.
    """

    df[columns] = df[columns].astype("category")
    return df


def process_null_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows with null values from the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame from which to remove null values.

    Returns:
    pd.DataFrame: The DataFrame after removing rows with null values.
    """

    res = df.dropna()
    return res


def drop_outliers(
    df: pd.DataFrame, threshold: int = 3, columns: list = None
) -> pd.DataFrame:
    """
    Remove outliers from specified columns in a DataFrame using Z-scores.

    Parameters:
    df (pd.DataFrame): The DataFrame from which to drop outliers.
    threshold (int): The Z-score threshold above which values are considered outliers.
                     Default is 3.

                     columns (list): A list of column names to check for outliers.

                     Returns:
                     pd.DataFrame: The DataFrame after removing outliers.
    """

    # Calculate Z-scores
    z_scores = np.abs(stats.zscore(df[columns]))

    # Create a boolean mask for rows that are not outliers
    mask = (z_scores < threshold).all(axis=1)

    # Filter the DataFrame to remove outliers
    return df[mask]


def remove_columns(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """
    Remove specified columns from a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame from which to remove columns.
    columns (list): A list of column names to remove.

    Returns:
    pd.DataFrame: The modified DataFrame after removing specified columns.
    """
    res = df.drop(columns=columns)
    return res
