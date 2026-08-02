import unittest
import os
import pandas as pd
import numpy as np
from data_cleaner import audit_and_clean_telemetry


class TestCleaner(unittest.TestCase):
    def setUp(self):
        self.dirty = "test_dirty.xlsx"
        self.clean = "test_clean.xlsx"
        pd.DataFrame(
            {
                "Date": ["2026-08-01", "2026-08-01", "2026-08-02"],
                "Location": ["Zone A", "Zone A", "Zone B"],
                "Sensor_Value": [50.0, 50.0, np.nan],
            }
        ).to_excel(self.dirty, index=False)

    def tearDown(self):
        for path in (self.dirty, self.clean):
            if os.path.exists(path):
                os.remove(path)

    def test_drops_dupes_and_fills_nan(self):
        ok = audit_and_clean_telemetry(self.dirty, self.clean)
        self.assertTrue(ok)

        out = pd.read_excel(self.clean)
        self.assertEqual(len(out), 2)
        self.assertFalse(out["Sensor_Value"].isnull().any())
        self.assertEqual(out.loc[1, "Sensor_Value"], 50.0)

    def test_missing_file_returns_false(self):
        ok = audit_and_clean_telemetry("does_not_exist.xlsx", "nope.xlsx")
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
