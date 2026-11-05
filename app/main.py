
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Warehouse Demand Forecasting & Dynamic Pricing",
    description="Demand forecasting, inventory and dynamic pricing API",
    version="1.0"
)

# Load project data
pricing = pd.read_csv("data/pricing_plan_snapshot.csv")
predictions = pd.read_csv("data/valid_predictions.csv")
history = pd.read_csv("data/history_recent.csv")

# Convert dates
predictions["date"] = pd.to_datetime(predictions["date"])
history["date"] = pd.to_datetime(history["date"])

# Root endpoint
@app.get("/")
def home():
    return {
        "message": "Warehouse Demand Forecasting API is running"
    }

# Health check
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "snapshot_date": "2017-09-30"
    }

# Find a store-item combination
def get_row(store: int, item: int):
    row = pricing[
        (pricing["store"] == store) &
        (pricing["item"] == item)
    ]

    if row.empty:
        raise HTTPException(
            status_code=404,
            detail="Store-item combination not found"
        )

    return row.iloc[0]

# Price recommendation endpoint
@app.get("/price-suggestion")
def price_suggestion(store: int, item: int):

    row = get_row(store, item)

    return {
        "store": store,
        "item": item,
        "current_price": float(row["base_price"]),
        "suggested_price": float(row["suggested_price"]),
        "action": row["action"],
        "stock": int(row["current_stock"]),
        "forecast_14d_units": int(row["forecast_14d_units"]),
        "cover_days": float(row["cover_days"])
    }

# Historical and validation forecast endpoint
@app.get("/forecast")
def forecast(store: int, item: int, days: int = 14):

    if days < 1 or days > 92:
        raise HTTPException(
            status_code=400,
            detail="Days must be between 1 and 92"
        )

    get_row(store, item)

    hist = history[
        (history["store"] == store) &
        (history["item"] == item)
    ].tail(30)

    pred = predictions[
        (predictions["store"] == store) &
        (predictions["item"] == item)
    ].head(days)

    return {
        "store": store,
        "item": item,
        "history": hist.to_dict(orient="records"),
        "forecast": pred.to_dict(orient="records")
    }

# What-if request model
class WhatIfRequest(BaseModel):
    store: int
    item: int
    new_price: float = Field(gt=0)
    elasticity: float | None = None

# What-if pricing simulator
@app.post("/whatif")
def whatif(request: WhatIfRequest):

    row = get_row(request.store, request.item)

    old_price = float(row["base_price"])
    new_price = request.new_price
    stock = int(row["current_stock"])
    old_units = min(int(row["forecast_14d_units"]), stock)

    elasticity = (
        request.elasticity
        if request.elasticity is not None
        else float(row["elasticity"])
    )

    # Price elasticity demand formula
    new_demand = (
        float(row["forecast_14d_units"]) *
        (new_price / old_price) ** elasticity
    )

    new_units = min(max(round(new_demand), 0), stock)

    cost = float(row["unit_cost"])

    old_revenue = old_units * old_price
    new_revenue = new_units * new_price

    old_profit = old_units * (old_price - cost)
    new_profit = new_units * (new_price - cost)

    return {
        "store": request.store,
        "item": request.item,
        "elasticity_used": elasticity,
        "old_price": round(old_price, 2),
        "new_price": round(new_price, 2),
        "old_units": old_units,
        "new_units": new_units,
        "old_revenue": round(old_revenue, 2),
        "new_revenue": round(new_revenue, 2),
        "old_profit": round(old_profit, 2),
        "new_profit": round(new_profit, 2),
        "revenue_change_percent": round(
            (new_revenue - old_revenue) / old_revenue * 100, 2
        ) if old_revenue else 0,
        "profit_change_percent": round(
            (new_profit - old_profit) / abs(old_profit) * 100, 2
        ) if old_profit else 0,
        "warning": (
            "Price is below unit cost"
            if new_price < cost else None
        )
    }
