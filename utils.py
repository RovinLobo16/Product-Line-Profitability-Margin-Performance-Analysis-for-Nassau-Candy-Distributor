import pandas as pd
import logging

# =========================
# SETUP LOGGER (PRO LEVEL)
# =========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data(filepath="Nassau Candy Distributor.csv"):
    try:
        # =========================
        # LOAD DATA
        # =========================
        df = pd.read_csv(filepath)
        logger.info("✅ Data loaded successfully")

        # =========================
        # CLEAN COLUMN NAMES
        # =========================
        df.columns = df.columns.str.strip().str.replace("\n", " ")

        # =========================
        # REQUIRED COLUMNS CHECK
        # =========================
        required_cols = ["Sales", "Units", "Gross Profit"]
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        # =========================
        # TYPE CONVERSION (SAFE)
        # =========================
        numeric_cols = ["Sales", "Units", "Gross Profit", "Cost"]

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # =========================
        # HANDLE MISSING VALUES
        # =========================
        before_rows = len(df)
        df = df.dropna(subset=["Sales", "Units", "Gross Profit"])
        logger.info(f"Removed {before_rows - len(df)} rows with missing values")

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
        # OPTIONAL: CAP EXTREME OUTLIERS (PRO FEATURE)
        # =========================
        if "Gross Margin %" in df.columns:
            df["Gross Margin %"] = df["Gross Margin %"].clip(-100, 100)

        # =========================
        # DATE HANDLING
        # =========================
        date_cols = ["Order Date", "Ship Date"]

        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        # =========================
        # DERIVED TIME FEATURES
        # =========================
        if "Order Date" in df.columns:
            df["Year"] = df["Order Date"].dt.year
            df["Month"] = df["Order Date"].dt.month
            df["Quarter"] = df["Order Date"].dt.to_period("Q").astype(str)

        # =========================
        # SORTING
        # =========================
        df = df.sort_values(by="Gross Profit", ascending=False)

        logger.info(f"✅ Final dataset shape: {df.shape}")

        return df

    except FileNotFoundError:
        logger.error("❌ File not found. Check your file path.")
        return pd.DataFrame()

    except ValueError as ve:
        logger.error(f"❌ Data validation error: {ve}")
        return pd.DataFrame()

    except Exception as e:
        logger.exception(f"❌ Unexpected error: {e}")
        return pd.DataFrame()
