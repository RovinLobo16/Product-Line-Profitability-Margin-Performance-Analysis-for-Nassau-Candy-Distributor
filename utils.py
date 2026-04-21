import pandas as pd

def load_data():
    df = pd.read_csv("data/Nassau Candy Distributor(5).csv")

    df = df[(df["Sales"] > 0) & (df["Units"] > 0)]

    df["Gross Margin %"] = (df["Gross Profit"] / df["Sales"]) * 100
    df["Profit per Unit"] = df["Gross Profit"] / df["Units"]

    return df
