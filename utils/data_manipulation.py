import numpy as np
import pandas as pd
from scipy import stats


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


def remove_columns(df: pd.DataFrame, columns: list = None):
    res = df.drop(columns=columns)
    return res
