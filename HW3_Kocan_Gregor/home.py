import streamlit as st
import pandas as pd

st.title("Financial Transactions Dashboard")

st.write("""
Welcome to the Financial Transactions Dashboard.

Use the menu on the left to navigate between the analytical pages:

**Page 1 – Time Analysis**  
Explore how the number of transactions changes over time. You can filter the results by date range and view the most traded symbols, sectors, and industries.

**Page 2 – Country Analysis**  
Analyze transactions by selected country. This page shows transaction trends and the top industries for BUY and SELL transactions.

The dashboard is interactive, so charts update automatically based on the selected filters.
""")

transactions = pd.read_csv("account-statement-1-1-2024-12-31-2024.csv", sep=";")
symbols = pd.read_csv("symbols.csv", sep=";")
countries = pd.read_csv("country.csv", sep=";")