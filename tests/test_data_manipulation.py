import numpy as np
import pandas as pd
import pytest
import repackage

repackage.up()
from utils.data_manipulation import (  # Replace with your actual module name
    drop_outliers,
    get_categorical,
    process_null_values,
    remove_columns,
)


# Sample DataFrame for testing
@pytest.fixture(scope="module")
def sample_df():
    """Fixture to provide a sample DataFrame for testing."""
    data = {
        "A": [1, 2, 3, np.nan, 5],
        "B": ["a", "b", "c", "d", "e"],
        "C": [10, 20, 30, 40, 50],
    }
    return pd.DataFrame(data)


def test_get_categorical(sample_df):
    """Test get_categorical function."""
    df = get_categorical(sample_df, columns=["B"])

    # Check if column B is of categorical type
    assert df["B"].dtype.name == "category", "Column B should be categorical."


def test_process_null_values(sample_df):
    """Test process_null_values function."""
    df = process_null_values(sample_df)

    # Check if the row with NaN in column A is removed
    assert df.shape[0] == 4, "There should be 4 rows after removing null values."
    assert (
        df.isnull().sum().sum() == 0
    ), "There should be no null values in the DataFrame."


def test_drop_outliers(sample_df):
    """Test drop_outliers function."""
    # Add outlier to column C
    sample_df.loc[5] = [6, "f", 1000]  # Adding an outlier
    df = drop_outliers(sample_df, threshold=2, columns=["C"])

    # Check that the outlier is removed
    assert df.shape[0] == 5, "There should be 5 rows after dropping outliers."


def test_remove_columns(sample_df):
    """Test remove_columns function."""
    df = remove_columns(sample_df, columns=["B"])

    # Check if column B is removed
    assert "B" not in df.columns, "Column B should be removed from the DataFrame."
    assert df.shape[1] == 2, "There should be 2 columns left in the DataFrame."


if __name__ == "__main__":
    pytest.main()
