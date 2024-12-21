import pandas as pd


def get_dataframe_to_plot(name: str = "housing data") -> pd.DataFrame:
    if name.lower() == "housing data":
        from data_queries.housing_queries import build_plot_df

        return build_plot_df()
    elif name.lower() == "credit risk":
        from data_queries.credit_risk_queries import build_plot_df

        return build_plot_df()
    else:
        raise ValueError("Dataset not available.")
