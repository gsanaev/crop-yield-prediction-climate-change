# src/crop/merge_data.py

import os
import pandas as pd

RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")


def _ensure_directories():
    os.makedirs(PROCESSED_DIR, exist_ok=True)


def merge_datasets(
    wdi_file="wdi_data.csv",
    nasa_file="nasa_data.csv",
    output_file="wdi_nasa.csv",
    replace=True
) -> str:
    """
    Merge World Bank (WDI) and NASA climate datasets into a single tidy CSV.
    """
    _ensure_directories()

    wdi_path = os.path.join(RAW_DIR, wdi_file)
    nasa_path = os.path.join(RAW_DIR, nasa_file)
    output_path = os.path.join(PROCESSED_DIR, output_file)

    if os.path.exists(output_path) and not replace:
        print(f"File already exists, skipping merge: {output_path}")
        return output_path

    # Load WDI data (country-level, many predictors)
    wdi = pd.read_csv(wdi_path)

    # Load NASA data (global anomalies, year-level only)
    nasa = pd.read_csv(nasa_path)

    # Merge on year (NASA has no country dimension)
    merged = pd.merge(
        wdi,
        nasa,
        on="year",
        how="left"
    )

    # Save final dataset
    merged.to_csv(output_path, index=False)
    print(f"✅ Final merged dataset → {output_path} ({len(merged)} rows)")
    print(merged.head())

    return output_path


if __name__ == "__main__":
    merge_datasets(replace=True)
