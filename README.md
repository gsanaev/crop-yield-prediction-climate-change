# 🌾 Crop Yield Prediction under Climate Change with Machine Learning 🚀

> A reproducible machine learning pipeline to predict national crop yields under changing climatic and agricultural conditions.  
> Built with Ridge Regression and Random Forest models, integrating temperature, precipitation, and fertilizer data.

![Python Version](https://img.shields.io/badge/python-3.10-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/status-completed-success)

## 📘 View Results Online

You can explore the full analysis directly here:

- [📈 Descriptive Statistics](https://gsanaev.github.io/crop-yield-prediction-climate-change/01-exploration.html)
- [⚙️ Modeling Summary](https://gsanaev.github.io/crop-yield-prediction-climate-change/04-modeling.html)
- [📊 Evaluation Results](https://gsanaev.github.io/crop-yield-prediction-climate-change/05-evaluation.html)
- [🌍 Final Report](https://gsanaev.github.io/crop-yield-prediction-climate-change/07-report.html)

---

## 📊 Project Overview

**Problem Statement:**  
Climate change is reshaping agricultural productivity across regions, yet the impact varies by country and year. Understanding and quantifying these effects at the national level is critical for climate-resilient planning and food security.

**Goal:**  
To build a reproducible modeling pipeline that predicts crop yields by country and year, evaluates model performance over time, and generates scenario-based projections (t and t+1) under climate change assumptions.

**Methods:**  
- Automated data extraction from external APIs (World Bank WDI and NASA POWER)  
- Time-aware regression models (Ridge and Random Forest)  
- Lagged, nonlinear, and interaction feature engineering  
- Cross-validation and hold-out testing (last 5 years)  
- Scenario-based yield projections and robust spatial visualization  

---

## 🎯 Key Findings

- 📈 **High predictive accuracy:** Ridge model achieved R² ≈ 0.93 (CV) and 0.94 (hold-out), with MAE ≈ 273–377 kg/ha.  
- 🔍 **Stable generalization:** Strong hold-out performance (2018–2022) confirms robustness against temporal drift.  
- 💡 **Feature sensitivity:** Temperature–precipitation and fertilizer interactions explain most interannual variability.  
- 🌍 **Scenario insight:** Modest short-term yield deltas, with some regional heterogeneity captured better by RF.  
- 🗺️ **Balanced visualization:** Δ% choropleths use symmetric color scales for unbiased interpretation of spatial change.

---

## 📁 Repository Structure

```
├── data/
│   ├── raw/                        # Downloaded raw data
│   │   ├── wdi_data.csv            # Extracted from WDI API
│   │   └── nasa_data.csv           # Extracted from NASA POWER API
│   ├── processed/
│   │   └── wdi_nasa.csv            # Merged dataset (output of merge_data.py)
│   ├── countries_preprocessed.csv  # Cleaned data (output of notebook 02)
│   └── countries_features.csv      # Engineered features (output of notebook 03)
├── src/
│   └── crop/
│       ├── wdi_data.py             # Extracts agricultural indicators from World Bank WDI API
│       ├── nasa_data.py            # Downloads climate data (temperature, precipitation) from NASA POWER API
│       └── merge_data.py           # Harmonizes and merges WDI and NASA data into unified dataset
├── artifacts/
│   ├── ridge.joblib
│   └── rf.joblib                   # Trained model artifacts
├── reports/
│   ├── metrics/                    # Model performance metrics
│   ├── predictions/                # Country-level predictions
│   └── scenarios/                  # Scenario outputs (t/t+1 per model)
├── notebooks/
│   ├── 01-exploration.ipynb        # Data audit and completeness
│   ├── 02-preprocessing.ipynb      # Cleaning and harmonization
│   ├── 03-feature-engineering.ipynb# Lags, rolls, nonlinearities
│   ├── 04-modeling.ipynb           # Ridge & RF training and diagnostics
│   ├── 05-evaluation.ipynb         # Metrics and model comparison
│   ├── 06-scenario_analysis.ipynb  # Scenario projections (t and t+1)
│   └── 07-report.ipynb             # Summary tables and choropleth maps
├── README.md
└── docs/                           # Supporting documentation
```

---

## 🔧 Technologies Used

**Programming languages:**  
- Python 3.12

**Libraries & frameworks:**  
- `pandas`, `numpy`  
- `scikit-learn` (Ridge, RandomForestRegressor, pipelines)  
- `matplotlib` for visualization  
- `joblib` for model persistence  
- `requests`, `xmltodict`, `tqdm` (for API data extraction)

**Tools:**  
- JupyterLab / VS Code  
- Git & version control  
- HTML/CSV reporting

---

## 📊 Data

**Data source:**  
- 🌐 **World Bank WDI API:** Agricultural and economic indicators  
- ☀️ **NASA POWER API:** Climate data (temperature, precipitation)  
- 🔗 **Merge pipeline:** Harmonized by `merge_data.py`  

**Dataset Size:**  
216 country–year observations after filtering (countries only; aggregates removed).

**Key Features:**  
- **Yield (target):** crop yield in kg/ha  
- **Climate:** annual mean temperature, precipitation, anomalies  
- **Inputs:** fertilizer application (kg/ha)  
- **Derived:** log/square terms, lag-1 features, and interactions

---

## 🧩 Data Extraction Workflow

The raw data extraction and merging steps are performed using Python modules located in `src/crop/`.

### Step 1 — Extract World Bank Data
```bash
uv run python -m src.crop.wdi_data
```
Downloads agricultural and economic indicators from the **World Bank WDI API**.  
Output: `data/raw/wdi_data.csv`

### Step 2 — Extract NASA POWER Climate Data
```bash
uv run python -m src.crop.nasa_data
```
Downloads temperature and precipitation data from **NASA POWER API**.  
Output: `data/raw/nasa_data.csv`

### Step 3 — Merge the Datasets
```bash
uv run python -m src.crop.merge_data
```
Merges WDI and NASA data by ISO3 and year.  
Output: `data/processed/wdi_nasa.csv`

---

## 🤖 Methodology

### Data Preprocessing
- Filtering out aggregates and incomplete entries  
- Harmonizing country identifiers and time coverage  
- No imputation of target variable (strict time-aware CV)

### Modeling Approach
- **Ridge Regression (primary):** interpretable linear model with L2 regularization  
- **Random Forest (optional):** nonlinear model for heterogeneous scenario analysis  
- Both models embedded in `Pipeline` with `SimpleImputer` and `StandardScaler`

### Evaluation
- 5-fold **TimeSeriesSplit** cross-validation  
- **Hold-out** (2018–2022) for temporal generalization  
- Metrics: R², MAE, RMSE  
- Ridge chosen as baseline for diagnostics and reporting

---

## 📈 Results

**Model Performance:**
| Model | Split | R² | MAE (kg/ha) | RMSE (kg/ha) |
|--------|-------|----|--------------|---------------|
| Ridge | Cross-validation | 0.927 | 273 | 615 |
| Ridge | Hold-out (2018–2022) | 0.944 | 377 | 810 |

**Most important visualizations:**
- Feature importance bar plots (04-modeling)  
- Temporal prediction vs. actual yield curves (05-evaluation)  
- Scenario Δ% choropleth (07-report)

---

## 🚀 Reproducibility

This project uses **[uv](https://docs.astral.sh/uv/)** for environment and dependency management.

### Setup
```bash
# Clone repository
git clone https://github.com/gsanaev/crop-yield-prediction-climate-change.git
cd crop-yield-prediction-climate-change

# Sync environment (installs Python + dependencies automatically)
uv sync
```

`uv sync` ensures:
- The correct Python version is installed  
- All dependencies are set up inside `.venv`  
- The project is immediately ready to run  

### Execution
```bash
# Step 1. Extract data
uv run python -m src.crop.wdi_data
uv run python -m src.crop.nasa_data
uv run python -m src.crop.merge_data

# Step 2. Run notebooks in sequence
# 1. notebooks/01-exploration.ipynb
# 2. notebooks/02-preprocessing.ipynb
# 3. notebooks/03-feature-engineering.ipynb
# 4. notebooks/04-modeling.ipynb
# 5. notebooks/05-evaluation.ipynb
# 6. notebooks/06-scenario_analysis.ipynb
# 7. notebooks/07-report.ipynb
```

---

## 🎓 About This Project

**Context:**  
Research project on climate-driven agricultural modeling. Designed for reproducibility, diagnostics, and scenario analysis.

**Date:**  
2025

**Author:**  
Golib Sanaev

## 📞 Contact

**GitHub:** [@gsanaev](https://github.com/gsanaev)  
**E-Mail:** gsanaev80@gmail.com  
**LinkedIn:** [golib-sanaev](https://linkedin.com/in/golib-sanaev/)

---

## 🙏 Acknowledgements

- [StackFuel](https://stackfuel.com/de/) Team — for inspiring and supporting data-driven learning in applied machine learning and analytics  
- World Bank and NASA — for providing open climate and agricultural data sources  
- scikit-learn & SHAP communities — for robust, transparent machine learning tools  

---

**⭐ If you find this project interesting, please give it a star!**
