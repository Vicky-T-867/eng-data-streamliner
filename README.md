# Data Streamliner

Small Python toolkit for cleaning telemetry spreadsheets, stitching daily logs together, and knocking out basic status reports. Handy when you're stuck merging Excel dumps by hand.

## What it does

- **`batch_consolidator.py`** — grabs every `.xlsx` in a folder, stacks them, tags each row with its source file
- **`data_cleaner.py`** — drops duplicates, fills missing sensor values, coerces junk text to numbers
- **`report_generator.py`** — flags readings over a threshold, plots a quick chart, writes a Word summary
- **`auto_filler.py`** — fills a fixed inspection template and highlights breached values
- **`test_pipeline.py`** — a couple of unit tests around the cleaner

## Setup

```bash
pip install pandas matplotlib python-docx openpyxl numpy
```

You'll also want the sample files in the repo root (`dummy_data.xlsx`, `inspection_template.xlsx`).

## Run

```bash
python3 batch_consolidator.py
python3 data_cleaner.py
python3 report_generator.py
python3 auto_filler.py
python3 test_pipeline.py
```

Order isn't strict — each script can run on its own with the sample inputs.

## License

MIT — see [LICENSE](LICENSE).
