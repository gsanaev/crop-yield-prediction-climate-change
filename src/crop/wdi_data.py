import os
import requests
import zipfile
import pandas as pd

RAW_DIR = os.path.join("data", "raw")


def _ensure_directories():
    os.makedirs(RAW_DIR, exist_ok=True)


def download_wdi_bulk(url="http://databank.worldbank.org/data/download/WDI_CSV.zip",
                      filename="WDI_CSV.zip",
                      replace=False) -> str:
    """
    Download the World Bank WDI bulk dataset (CSV ZIP).
    """
    _ensure_directories()
    zip_path = os.path.join(RAW_DIR, filename)

    if os.path.exists(zip_path) and not replace:
        print(f"File already exists, skipping download: {zip_path}")
        return zip_path

    print("⬇️ Downloading World Bank WDI bulk dataset...")
    response = requests.get(url)
    response.raise_for_status()

    with open(zip_path, "wb") as f:
        f.write(response.content)

    print(f"✅ Saved WDI bulk ZIP to {zip_path}")
    return zip_path


def extract_indicators(zip_path,
                       indicators: dict,
                       filename="wdi_data.csv",
                       replace=False,
                       delete_zip=True) -> str:
    """
    Extract selected indicators from WDI bulk dataset and save tidy CSV.
    """
    output_path = os.path.join(RAW_DIR, filename)
    if os.path.exists(output_path) and not replace:
        print(f"File already exists, skipping extraction: {output_path}")
        return output_path

    with zipfile.ZipFile(zip_path, "r") as z:
        # Find the main dataset file (currently WDICSV.csv)
        data_file = [
            f for f in z.namelist()
            if f.upper().endswith("CSV.CSV")  # WDICSV.csv
            and "COUNTRY" not in f.upper()
            and "SERIES" not in f.upper()
            and "FOOTNOTE" not in f.upper()
        ]
        if not data_file:
            raise FileNotFoundError("Could not find main data CSV inside WDI ZIP")
        data_file = data_file[0]
        print(f"📂 Found data file inside ZIP: {data_file}")

        with z.open(data_file) as f:
            df = pd.read_csv(f)

    # Filter only selected indicators
    df = df[df["Indicator Code"].isin(indicators.keys())]

    # Reshape wide → long
    df_long = df.melt(
        id_vars=["Country Name", "Country Code", "Indicator Code"],
        var_name="year",
        value_name="value"
    )

    # Keep only numeric years
    df_long = df_long[df_long["year"].str.isnumeric()]
    df_long["year"] = df_long["year"].astype(int)

    # Pivot indicators into columns
    df_pivot = df_long.pivot_table(
        index=["Country Name", "Country Code", "year"],
        columns="Indicator Code",
        values="value"
    ).reset_index()

    # Rename codes → user-friendly names
    df_pivot = df_pivot.rename(columns=indicators)

    # Save tidy dataset
    df_pivot.to_csv(output_path, index=False)
    print(f"✅ Extracted indicators → {output_path} ({len(df_pivot)} rows)")
    print(df_pivot.head())

    # Optional: delete ZIP
    if delete_zip and os.path.exists(zip_path):
        os.remove(zip_path)
        print(f"🗑️ Deleted ZIP file: {zip_path}")

    return output_path


if __name__ == "__main__":
    indicators = {
        # 🌾 Agriculture
        "AG.YLD.CREL.KG": "cereal_yield",        # target
        "AG.LND.PRCP.MM": "precipitation",       # climate
        "AG.CON.FERT.ZS": "fertilizer_use",      # inputs

        # 🌍 Climate & Environment
        "EN.GHG.CO2.MT.CE.AR5": "co2_total_mt",   # CO₂ total (Mt, excl. LULUCF)
        "EN.GHG.CO2.PC.CE.AR5": "co2_per_capita", # CO₂ per capita (tons/person, excl. LULUCF)
        "AG.LND.FRST.ZS": "forest_area_pct",      # Forest area (% of land)

        # 👥 Socio-Economic
        "NY.GDP.PCAP.CD": "gdp_per_capita",       # economy
        "SP.POP.TOTL": "population",              # population
        "SP.RUR.TOTL.ZS": "rural_pop_pct",        # Rural population (%)
        "SL.AGR.EMPL.ZS": "agri_employment_pct",  # Agri employment (% of total)

        # 🌱 Land & Irrigation
        "AG.LND.ARBL.ZS": "arable_land_pct",      # Arable land (% of land area)
        "AG.LND.IRIG.AG.ZS": "irrigated_land_pct" # Irrigated land (% of arable land)
    }

    zip_path = download_wdi_bulk(replace=False)
    extract_indicators(
        zip_path,
        indicators,
        filename="wdi_data.csv",
        replace=True,
        delete_zip=True
    )
