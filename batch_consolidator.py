import os
import glob
import pandas as pd


def consolidate_daily_logs(source_folder, merged_output_file):
    """Merge all .xlsx files in a folder into one spreadsheet."""
    print(f"Scanning {source_folder} for Excel logs...")

    files = glob.glob(os.path.join(source_folder, "*.xlsx"))
    if not files:
        print(f"No .xlsx files in '{source_folder}'.")
        return False

    print(f"Found {len(files)} file(s).")

    frames = []
    for path in files:
        name = os.path.basename(path)
        try:
            df = pd.read_excel(path)
            df["Source_Log_File"] = name
            frames.append(df)
            print(f"  loaded {name}")
        except Exception as e:
            print(f"  skipped {name}: {e}")

    if not frames:
        print("Nothing readable — aborting.")
        return False

    master = pd.concat(frames, ignore_index=True)
    master.to_excel(merged_output_file, index=False)
    print(f"Wrote {len(master)} rows to {merged_output_file}\n")
    return True


if __name__ == "__main__":
    mock_dir = "daily_sensor_logs"
    os.makedirs(mock_dir, exist_ok=True)

    pd.DataFrame(
        {"Date": ["2026-08-01"], "Location": ["Station A"], "Sensor_Value": [72.3]}
    ).to_excel(os.path.join(mock_dir, "log_20260801.xlsx"), index=False)
    pd.DataFrame(
        {"Date": ["2026-08-02"], "Location": ["Station B"], "Sensor_Value": [81.5]}
    ).to_excel(os.path.join(mock_dir, "log_20260802.xlsx"), index=False)
    pd.DataFrame(
        {"Date": ["2026-08-03"], "Location": ["Station C"], "Sensor_Value": [64.0]}
    ).to_excel(os.path.join(mock_dir, "log_20260803.xlsx"), index=False)

    consolidate_daily_logs(
        source_folder=mock_dir,
        merged_output_file="consolidated_raw_master.xlsx",
    )
