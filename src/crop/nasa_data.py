import os
import requests
import pandas as pd
from io import StringIO

RAW_DIR = os.path.join("data", "raw")

def _ensure_directories():
    os.makedirs(RAW_DIR, exist_ok=True)


def fetch_temperature():
    """
    Fetch NASA GISTEMP global temperature anomaly dataset (annual mean).
    """
    url = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
    print("⬇️ Downloading NASA GISTEMP temperature anomalies...")

    response = requests.get(url)
    response.raise_for_status()

    # NASA table: columns by month + J-D (annual mean), DJF, etc.
    df = pd.read_csv(StringIO(response.text), skiprows=1)

    # Extract only Year and J-D (annual mean anomaly)
    df = df.rename(columns={"Year": "year", "J-D": "temp_anomaly"})
    df = df[["year", "temp_anomaly"]].dropna()

    # Convert types
    df["year"] = df["year"].astype(int)
    df["temp_anomaly"] = pd.to_numeric(df["temp_anomaly"], errors="coerce")

    return df


def fetch_nasa_temperature(filename="nasa_data.csv", replace=False):
    """
    Fetch NASA GISTEMP anomalies and save to CSV.
    """
    _ensure_directories()
    output_path = os.path.join(RAW_DIR, filename)

    if os.path.exists(output_path) and not replace:
        print(f"File already exists, skipping: {output_path}")
        return output_path

    df = fetch_temperature()
    df.to_csv(output_path, index=False)

    print(f"✅ Cleaned NASA temperature anomalies saved → {output_path}")
    return output_path


if __name__ == "__main__":
    fetch_nasa_temperature(replace=True)
