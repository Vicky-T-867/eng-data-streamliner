import pandas as pd
import numpy as np


def audit_and_clean_telemetry(input_file, output_file):
    """Drop dupes, fill missing sensor values, coerce bad types."""
    print(f"Cleaning {input_file}...")

    try:
        df = pd.read_excel(input_file)
        initial_rows = len(df)

        df.drop_duplicates(inplace=True)
        dupes = initial_rows - len(df)
        if dupes:
            print(f"Removed {dupes} duplicate row(s).")

        # coerce junk text first so mean() doesn't blow up on mixed types
        before_na = df["Sensor_Value"].isnull().sum()
        df["Sensor_Value"] = pd.to_numeric(df["Sensor_Value"], errors="coerce")
        coerced = df["Sensor_Value"].isnull().sum() - before_na
        if coerced > 0:
            print(f"Coerced {coerced} non-numeric value(s) to NaN.")

        if df["Sensor_Value"].isnull().any():
            missing = df["Sensor_Value"].isnull().sum()
            fill = df["Sensor_Value"].mean()
            if pd.isnull(fill):
                fill = 0
            df["Sensor_Value"] = df["Sensor_Value"].fillna(fill)
            print(f"Filled {missing} missing value(s) with mean ({fill:.2f}).")

        df.to_excel(output_file, index=False)
        print(f"Wrote cleaned data to {output_file}\n")
        return True

    except FileNotFoundError:
        print(f"File not found: {input_file}")
        return False
    except Exception as e:
        print(f"Clean failed: {e}")
        return False


if __name__ == "__main__":
    # quick dirty sample to exercise the cleaner
    dirty = pd.DataFrame(
        {
            "Date": ["2026-08-01", "2026-08-01", "2026-08-02", "2026-08-03", "2026-08-04"],
            "Location": ["Site A", "Site A", "Site B", "Site C", "Site D"],
            "Sensor_Value": [45.5, 45.5, np.nan, "MALFUNCTION_TEXT", 92.1],
        }
    )
    dirty.to_excel("dirty_telemetry_logs.xlsx", index=False)

    audit_and_clean_telemetry(
        input_file="dirty_telemetry_logs.xlsx",
        output_file="production_clean_data.xlsx",
    )
