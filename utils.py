import pandas as pd

def load_data(filepath="Nassau Candy Distributor.csv"):
    try:
        # =========================
        # LOAD DATA
        # =========================
        df = pd.read_csv(filepath)

        # =========================
        # STANDARDIZE COLUMN NAMES
        # =========================
        df.columns = df.columns.str.strip()

        # =========================
        # TYPE CONVERSION
        # =========================
        numeric_cols = ["Sales", "Units", "Gross Profit", "Cost"]

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # =========================
        # HANDLE MISSING VALUES
        # =========================
        df = df.dropna(subset=["Sales", "Units", "Gross Profit"])

        # =========================
        # REMOVE INVALID DATA
        # =========================
        df = df[(df["Sales"] > 0) & (df["Units"] > 0)]

        # =========================
        # FEATURE ENGINEERING
        # =========================
        df["Gross Margin %"] = (df["Gross Profit"] / df["Sales"]) * 100
        df["Profit per Unit"] = df["Gross Profit"] / df["Units"]

        # =========================
        # DATE HANDLING (if exists)
        # =========================
        if "Order Date" in df.columns:
            df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

        # =========================
        # SORT DATA (optional but useful)
        # =========================
        df = df.sort_values(by="Gross Profit", ascending=False)

        return df

    except FileNotFoundError:
        print("❌ File not found. Check your path.")
        return pd.DataFrame()

    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return pd.DataFrame()
