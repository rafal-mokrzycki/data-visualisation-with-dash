import pandas as pd
import pytest
import repackage
from pytest_mock import MockerFixture

repackage.up()
from data.get_data import get_dataframe_to_plot


@pytest.fixture(scope="module")
def housing_data():
    yield pd.DataFrame(
        {
            "price": [200000, 250000, 300000],
            "size": [1500, 1800, 2400],
        }
    )


@pytest.fixture(scope="module")
def credit_risk_data():
    yield pd.DataFrame(
        {
            "loan_amount": [10000, 20000, 30000],
            "default": [0, 1, 0],
        }
    )


def test_get_dataframe_to_plot_housing_data(housing_data, mocker: MockerFixture):
    """Test retrieving housing data."""
    with mocker.patch(
        "data_queries.housing_queries.build_plot_df", return_value=housing_data
    ):
        df = get_dataframe_to_plot("housing data")
        assert isinstance(df, pd.DataFrame), "Returned value should be a DataFrame."
        assert df.equals(
            housing_data
        ), "The returned DataFrame should match the expected housing data."


def test_get_dataframe_to_plot_credit_risk(credit_risk_data, mocker: MockerFixture):
    """Test retrieving credit risk data."""
    with mocker.patch(
        "data_queries.credit_risk_queries.build_plot_df", return_value=credit_risk_data
    ):
        df = get_dataframe_to_plot("credit risk")
        assert isinstance(df, pd.DataFrame), "Returned value should be a DataFrame."
        assert df.equals(
            credit_risk_data
        ), "The returned DataFrame should match the expected credit risk data."


def test_get_dataframe_to_plot_invalid_name():
    """Test retrieving data with an invalid dataset name."""
    with pytest.raises(ValueError, match="Dataset not available."):
        get_dataframe_to_plot("invalid dataset")


if __name__ == "__main__":
    pytest.main()
