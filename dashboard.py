
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Warehouse Demand & Dynamic Pricing",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Warehouse Demand Forecasting & Dynamic Pricing")
st.caption("AI-powered demand analysis, inventory monitoring and pricing decisions")

# Sidebar
st.sidebar.header("Product Selection")

store = st.sidebar.selectbox("Select Store", range(1, 11))
item = st.sidebar.selectbox("Select Item", range(1, 51))

# Fetch API data
try:
    price_response = requests.get(
        f"{API_URL}/price-suggestion",
        params={"store": store, "item": item},
        timeout=10
    )
    price_response.raise_for_status()
    price_data = price_response.json()

    forecast_response = requests.get(
        f"{API_URL}/forecast",
        params={"store": store, "item": item, "days": 14},
        timeout=10
    )
    forecast_response.raise_for_status()
    forecast_data = forecast_response.json()

except requests.RequestException as e:
    st.error(f"Could not connect to FastAPI: {e}")
    st.info("Make sure the FastAPI server is running on port 8000.")
    st.stop()

# Inventory and pricing metrics
st.subheader(f"Store {store} | Item {item}")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Current Price", f"₹{price_data['current_price']:.2f}")
c2.metric("Suggested Price", f"₹{price_data['suggested_price']:.2f}")
c3.metric("Current Stock", f"{price_data['stock']} units")
c4.metric("Stock Cover", f"{price_data['cover_days']:.2f} days")

action = price_data["action"]

st.markdown("### Pricing Recommendation")

if action == "RAISE":
    st.success(f"Recommended Action: {action}")
elif action.startswith("DISCOUNT"):
    st.warning(f"Recommended Action: {action}")
else:
    st.info(f"Recommended Action: {action}")

st.write(
    f"Expected 14-day demand: "
    f"**{price_data['forecast_14d_units']} units**"
)

# Forecast chart
st.markdown("---")
st.subheader("Demand Analysis")

history = pd.DataFrame(forecast_data["history"])
forecast = pd.DataFrame(forecast_data["forecast"])

history["date"] = pd.to_datetime(history["date"])
forecast["date"] = pd.to_datetime(forecast["date"])

fig, ax = plt.subplots(figsize=(12, 4))

ax.plot(
    history["date"], history["sales"],
    label="Historical Sales"
)

ax.plot(
    forecast["date"], forecast["predicted_sales"],
    label="Validation Predictions",
    linestyle="--"
)

ax.set_xlabel("Date")
ax.set_ylabel("Units Sold")
ax.set_title("Historical Sales vs Validation Predictions")
ax.legend()
ax.grid(alpha=0.3)

st.pyplot(fig)
plt.close(fig)

st.caption(
    "Note: October predictions are historical validation results, "
    "not live future forecasts."
)

# What-if simulator
st.markdown("---")
st.subheader("What-If Pricing Simulator")

new_price = st.number_input(
    "Enter a new product price (₹)",
    min_value=1.0,
    value=float(price_data["current_price"]),
    step=5.0
)

if st.button("Simulate Price Change"):
    try:
        response = requests.post(
            f"{API_URL}/whatif",
            json={
                "store": store,
                "item": item,
                "new_price": new_price
            },
            timeout=10
        )
        response.raise_for_status()
        result = response.json()

        st.markdown("### Simulation Results")

        a, b, c = st.columns(3)

        a.metric(
            "Estimated Units Sold",
            result["new_units"],
            delta=result["new_units"] - result["old_units"]
        )

        b.metric(
            "Estimated Revenue",
            f"₹{result['new_revenue']:,.2f}",
            delta=f"{result['revenue_change_percent']}%"
        )

        c.metric(
            "Estimated Profit",
            f"₹{result['new_profit']:,.2f}",
            delta=f"{result['profit_change_percent']}%"
        )

        if result["warning"]:
            st.warning(result["warning"])

    except requests.RequestException as e:
        st.error(f"Simulation failed: {e}")

st.markdown("---")
st.caption("Warehouse Demand Forecasting & Dynamic Pricing | ML Mini Project")
