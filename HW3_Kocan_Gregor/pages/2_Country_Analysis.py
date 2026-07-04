import streamlit as st
import pandas as pd

st.title("Page 2 - Country Analysis")
st.write(
    "This page analyses transactions by selected country. "
    "All charts react to the selected country."
)

transactions = pd.read_csv("account-statement-1-1-2024-12-31-2024.csv", sep=";")
symbols = pd.read_csv("symbols.csv", sep=";")
countries = pd.read_csv("country.csv", sep=";")

transactions.columns = transactions.columns.str.strip()
symbols.columns = symbols.columns.str.strip()
countries.columns = countries.columns.str.strip()

symbols = symbols.rename(columns={"symbol": "Symbol"})

transactions["Date"] = pd.to_datetime(
    transactions["Date"],
    dayfirst=True,
    errors="coerce"
)

df = transactions.merge(symbols, on="Symbol", how="left")

st.subheader("Filters")
country_options = sorted(df["country"].dropna().unique())
selected_country = st.selectbox(
    "Select country",
    country_options
)

filtered = df[df["country"] == selected_country]

if filtered.empty:
    st.warning("No transactions exist for the selected country.")
    st.stop()

st.write(f"Transactions for selected country: **{len(filtered)}**")

st.divider()

st.subheader("Total transactions over time")
filtered["OnlyDate"] = filtered["Date"].dt.date

transactions_over_time = (
    filtered
    .groupby("OnlyDate")
    .size()
    .reset_index(name="Transaction count")
)

transactions_over_time = transactions_over_time.rename(columns={"OnlyDate": "Date"})

st.line_chart(
    transactions_over_time,
    x="Date",
    y="Transaction count"
)

st.subheader("Top industries by BUY transactions")
buy_df = filtered[filtered["TransactionType"] == "BUY"]

top_buy_industries = (
    buy_df
    .groupby("industry")
    .size()
    .reset_index(name="BUY transaction count")
    .sort_values("BUY transaction count", ascending=False)
    .head(10)
)

st.bar_chart(
    top_buy_industries,
    x="industry",
    y="BUY transaction count"
)

st.subheader("Top industries by SELL transactions")

sell_df = filtered[filtered["TransactionType"] == "SELL"]

top_sell_industries = (
    sell_df
    .groupby("industry")
    .size()
    .reset_index(name="SELL transaction count")
    .sort_values("SELL transaction count", ascending=False)
    .head(10)
)

st.bar_chart(
    top_sell_industries,
    x="industry",
    y="SELL transaction count"
)