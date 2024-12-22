import pandas as pd


def get_dataframe_to_plot(name: str = "housing data") -> pd.DataFrame:
    """
    Retrieve a DataFrame based on the specified dataset name.

    Parameters:
    name (str): The name of the dataset to retrieve. It can be either
                'housing data' or 'credit risk'.

    Returns:
    pd.DataFrame: The DataFrame corresponding to the selected dataset.

    Raises:
    ValueError: If the specified dataset name is not recognized.
    """
    if name.lower() == "housing data":
        from data_queries.housing_queries import build_plot_df

        return build_plot_df()
    elif name.lower() == "credit risk":
        from data_queries.credit_risk_queries import build_plot_df

        return build_plot_df()
    else:
        raise ValueError("Dataset not available.")
