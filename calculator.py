import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from datetime import datetime

# -------------------- API Setup --------------------
# API_KEY = "bc87829e1d2d4ee68dcbb775c90b598a"
VALUE_URL = "https://api.rentcast.io/v1/avm/value"
HEADERS = {"X-Api-Key": API_KEY}

def fetch_property_value(address):
    params = {"address": address}
    response = requests.get(VALUE_URL, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Value API Error {response.status_code}: {response.text}")
        return None

# -------------------- Page Config --------------------
st.set_page_config(page_title="Flipping and BRRRR Calculator", layout="wide")
st.title("Address-Based Home Value Estimator and Deal Analysis")

# -------------------- Tabs --------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "After Repair Value", 
    "Renovation", 
    "Flipping", 
    "Buy, Renovate, Rent, Refinance, Repeat"
])

# ================================================== Tab 1: After Repair Value ==================================================
with tab1:
    st.header("After Repair Value Estimation")

    address = st.text_input("Enter Property Address", "8018 Christmas Ct, Charlotte, NC 28316")

    if address:
        value_data = fetch_property_value(address)
        if value_data:
            rentcast_price = value_data.get("price")
            st.metric("RentCast Estimated Value", f"${rentcast_price:,.0f}")

# ====================================================== Tab 2: Renovation =================================================
with tab2:
    st.header("Renovation Costs Calculator")

    # Input Sliders
    bathrooms = st.slider("Bathrooms", 0, 10, 1)
    bedrooms = st.slider("Bedrooms", 0, 10, 1)
    square_footage = st.slider("Property Square Footage", 500, 10_000, 1500)
    windows = st.slider("Windows Being Replaced", 0, 20, 2)
    roof = st.slider("Replace Roof?", 0, 1, 1)  # 1 = yes
    hvac = st.slider("HVAC Units", 0, 3, 1)
    flooring = st.slider("Flooring (sqft)", 0, 10_000, 1000)
    kitchen = st.slider("Kitchen Remodel", 0, 1, 1)
    appliances = st.slider("Kitchen Appliances", 0, 1, 1)

    # Cost Calculation Logic
    cost_bathroom = bathrooms * 2000
    cost_bedroom = bedrooms * 1500
    cost_windows = windows * 500
    cost_roof = 0
    if roof:
        if square_footage < 1000:
            cost_roof = 6000
        elif square_footage > 2000:
            cost_roof = 10000
        else:
            cost_roof = 8000
    cost_hvac = hvac * 8000
    cost_flooring = flooring * 8
    cost_kitchen = kitchen * 5000
    cost_appliances = appliances * 2000

    # Total Rehab Cost
    total_rehab = (
        cost_bathroom + cost_bedroom + cost_windows +
        cost_roof + cost_hvac + cost_flooring +
        cost_kitchen + cost_appliances
    )

    # Output Results
    st.subheader("Estimated Renovation Cost Breakdown:")
    st.write(f"Bathrooms: ${cost_bathroom:,.0f}")
    st.write(f"Bedrooms: ${cost_bedroom:,.0f}")
    st.write(f"Windows: ${cost_windows:,.0f}")
    st.write(f"Roof: ${cost_roof:,.0f}")
    st.write(f"HVAC: ${cost_hvac:,.0f}")
    st.write(f"Flooring: ${cost_flooring:,.0f}")
    st.write(f"Kitchen Remodel: ${cost_kitchen:,.0f}")
    st.write(f"Kitchen Appliances: ${cost_appliances:,.0f}")

    st.metric("Total Rehab Estimate", f"${total_rehab:,.0f}")

# ================================================= Tab 3: Flipping ========================================
with tab3:
    st.header("Flipping Calculator")

    st.subheader("Is this a good deal?")
    
    purchase_price = st.number_input("Purchase Price", min_value=0, value=100000)
    minimum_desired_profit = st.number_input("Desired Profit", min_value=1000, max_value = purchase_price)
    selling_price = st.number_input("Expected Selling Price", min_value=0, value=150000)
    rehab_costs = st.number_input("Total Rehab Cost", min_value=0, value=total_rehab)
    closing_costs = st.number_input("Closing Costs", min_value=0, value=5000)
    holding_costs = st.number_input("Holding Costs", min_value=0, value=3000)

    total_investment = purchase_price + rehab_costs + closing_costs + holding_costs
    potential_profit = selling_price - total_investment

    st.metric("Total Investment", f"${total_investment:,.0f}")
    st.metric("Potential Profit", f"${potential_profit:,.0f}")

# =================================================== Tab 4: BRRRR ======================================
with tab4:
    st.header("Buy, Renovate, Rent, Refinance, Repeat (BRRRR)")

    st.subheader("Overview")
    st.markdown("""
    The BRRRR strategy involves purchasing undervalued properties, renovating them, renting them out, refinancing to pull equity out, and repeating the process.

    Use this section to analyze the viability of your BRRRR investment.
    """)

    purchase_price = st.number_input("Purchase= Tab 4: BRRRR ===== Price (BRRRR)", min_value=0, value=100000, key="brrrr_price")
    rehab_cost = st.number_input("Rehab Cost", min_value=0, value=total_rehab, key="brrrr_rehab")
    appraised_value = st.number_input("Appraised Value After Rehab", min_value=0, value=150000)
    refinance_percentage = st.slider("Refinance % of Appraised Value", 50, 100, 75)

    refinance_amount = appraised_value * (refinance_percentage / 100)
    total_cost = purchase_price + rehab_cost
    cash_out = refinance_amount - total_cost

    st.metric("Refinance Amount", f"${refinance_amount:,.0f}")
    st.metric("Total Cost", f"${total_cost:,.0f}")
    st.metric("Cash Out Refinance", f"${cash_out:,.0f}")

# -------------------- End --------------------
st.markdown("---")
st.caption("Created for real estate investors using RentCast API")
