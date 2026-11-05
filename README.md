# Warehouse Demand Forecasting & Dynamic Pricing

An ML-powered web application that forecasts product demand, monitors inventory risk, and provides dynamic pricing recommendations using historical sales data.

## Overview

This project combines machine learning, data analysis, and a web-based dashboard to support data-driven inventory and pricing decisions.

It uses a LightGBM regression model to predict product demand and a rule-based pricing engine to generate pricing recommendations based on estimated inventory coverage.

## Key Features

- **Demand Forecasting:** Predicts product-level demand using historical sales and time-based features.
- **Inventory Monitoring:** Displays available stock and estimated inventory coverage.
- **Dynamic Pricing:** Generates pricing recommendations based on inventory conditions and pricing rules.
- **What-if Simulation:** Evaluates how changes in product prices may affect demand, revenue, and profit.
- **Interactive Dashboard:** Visualizes forecasts, inventory information, pricing recommendations, and simulation results.
- **REST API:** Provides backend endpoints through FastAPI.

## Tech Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Machine Learning | LightGBM, Scikit-learn |
| Data Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Backend | FastAPI, Uvicorn |
| Frontend | Streamlit |
| Model Storage | Joblib |

## Model Performance

The LightGBM demand forecasting model was evaluated using a chronological train-validation split.

| Metric | Result |
|---|---:|
| MAE | 5.93 |
| RMSE | 7.69 |
| SMAPE | 12.48% |

The validation period covers October–December 2017.

**Note:** Validation uses rolling one-day-ahead predictions, with actual previous-day sales available when constructing subsequent validation features. These results should not be interpreted as a single 92-day forecast made in advance.

## Dataset

The project uses the Store Item Demand Forecasting Challenge dataset from Kaggle.

- 913,000 historical sales records
- 10 stores
- 50 products
- Daily sales data from 2013 to 2017

The pricing, product cost, elasticity, and inventory snapshot information used by the pricing and simulation modules is simulated for demonstration purposes.

## Project Structure

```text
warehouse-demand-pricing/
├── app/
│   ├── __init__.py
│   └── main.py
├── data/
├── models/
│   └── lgbm_demand.pkl
├── 01_data_exploration.ipynb.ipynb
├── dashboard.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/jatindahiya1502/warehouse-demand-forecasting-dynamic-pricing.git
cd warehouse-demand-forecasting-dynamic-pricing
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the FastAPI backend

```bash
uvicorn app.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

### 5. Start the Streamlit dashboard

Open a second terminal, activate the virtual environment, and run:

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API welcome endpoint |
| GET | `/health` | Health check |
| GET | `/forecast` | Demand forecast data |
| GET | `/price-suggestion` | Pricing recommendations |
| POST | `/whatif` | Price simulation |

## Future Improvements

- Deploy the application to a cloud platform.
- Integrate live inventory and sales data.
- Improve forecasting with additional models.
- Add automated low-stock alerts.
- Introduce more advanced price optimization techniques.

## Disclaimer

This project is developed for academic and portfolio purposes. Pricing, cost, elasticity, and inventory values are simulated. Model performance is based on the specified historical validation period and does not guarantee future forecasting accuracy.

## Author

**Jatin Dahiya**

GitHub: [@jatindahiya1502](https://github.com/jatindahiya1502)