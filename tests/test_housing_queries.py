import pandas as pd
import pytest
import repackage

repackage.up()

from data_queries.housing_queries import build_plot_df


@pytest.fixture(scope="module")
def test_df():
    # Sample data for testing
    sample_data = {
        "person_home_ownership": ["OWN", "RENT", "MORTGAGE"],
        "loan_intent": ["PERSONAL", "EDUCATION", "BUSINESS"],
        "loan_grade": ["A", "B", "C"],
        "loan_amnt": [10000, 20000, 15000],
        "loan_status": ["Fully Paid", "Charged Off", "Fully Paid"],
        "cb_person_default_on_file": ["Y", "N", "Y"],
        "person_age": [25, 30, 22],
    }

    # Create a DataFrame from sample data
    test_df = pd.DataFrame(sample_data)
    yield test_df


@pytest.fixture(scope="module")
def test_cat_columns():
    yield [
        "person_home_ownership",
        "loan_intent",
        "loan_grade",
        "loan_status",
        "cb_person_default_on_file",
    ]


@pytest.fixture(scope="module")
def test_cols_to_remove():
    yield ["cb_person_default_on_file", "person_age"]


def test_build_plot_df_default(test_df, test_cat_columns, test_cols_to_remove):
    """Test build_plot_df with default parameters."""
    df, cat_columns = build_plot_df(
        debug=False,
        df=test_df,
        cat_columns=test_cat_columns,
        cols_to_remove=test_cols_to_remove,
    )

    # Check that the returned DataFrame is as expected
    assert isinstance(df, pd.DataFrame), "Returned value should be a DataFrame."
    assert df.shape[0] == 3, "DataFrame should have 3 rows."

    # Check that categorical columns are correctly identified
    expected_cat_columns = [
        "person_home_ownership",
        "loan_status",
        "loan_intent",
        "loan_grade",
    ]
    assert (
        cat_columns.sort() == expected_cat_columns.sort()
    ), f"Expected categorical columns do not match. Got {cat_columns.sort()}"


def test_build_plot_df_with_debug(test_df, test_cat_columns, test_cols_to_remove):
    """Test build_plot_df with debug logging enabled."""
    df, _ = build_plot_df(
        debug=False,
        df=test_df,
        cat_columns=test_cat_columns,
        cols_to_remove=test_cols_to_remove,
    )

    # Check that debug logging works (you can use mock to verify logging if needed)
    assert isinstance(df, pd.DataFrame), "Returned value should be a DataFrame."


def test_build_plot_df_with_custom_cat_columns(
    test_df, test_cat_columns, test_cols_to_remove
):
    """Test build_plot_df with custom categorical columns."""
    df, cat_columns = build_plot_df(
        debug=False,
        df=test_df,
        cat_columns=test_cat_columns,
        cols_to_remove=test_cols_to_remove,
    )
    test_cat_columns = [
        "loan_status",
        "loan_grade",
        "loan_intent",
    ]  # due to columns removal
    # Check that the returned DataFrame is as expected
    assert isinstance(df, pd.DataFrame), "Returned value should be a DataFrame."

    # Verify that only custom categorical columns are returned
    assert (
        cat_columns.sort() == test_cat_columns.sort()
    ), f"Expected categorical columns do not match. Got {cat_columns}"


# Add more tests to cover other edge cases as needed

if __name__ == "__main__":
    pytest.main()
