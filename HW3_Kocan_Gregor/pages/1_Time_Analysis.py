import streamlit as st
import pandas as pd

st.title("Page 1 - Time Analysis")
st.write("This page provides a time-based analysis of financial transactions. "
         "Users can filter transactions by a selected date range and explore interactive visualizations showing "
         "transaction trends over time, as well as the most active symbols, sectors, and industries.")

transactions = pd.read_csv("account-statement-1-1-2024-12-31-2024.csv", sep=";")
symbols = pd.read_csv("symbols.csv", sep=";")
countries = pd.read_csv("country.csv", sep=";")

symbols = symbols.rename(columns={"symbol": "Symbol"})

transactions.columns = transactions.columns.str.strip()
symbols.columns = symbols.columns.str.strip()

transactions["Date"] = pd.to_datetime(
    transactions["Date"],
    dayfirst=True,
    errors="coerce"
)

df = transactions.merge(symbols, on="Symbol", how="left")

st.subheader("Filters")
col_start, col_end = st.columns(2)

with col_start:
    start_date = st.date_input(
        "Start date",
        value=pd.to_datetime("2024-01-01").date()
    )

with col_end:
    end_date = st.date_input(
        "End date",
        value=pd.to_datetime("2024-12-31").date()
    )

filtered = df[
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date)
]

st.write(f"Transactions in selected period: **{len(filtered)}**")
st.divider()

st.subheader("Total number of transactions over time")
filtered = filtered.copy()
filtered["OnlyDate"] = filtered["Date"].dt.date
transactions_over_time = (
    filtered
    .groupby("OnlyDate")
    .size()
    .reset_index(name="Transaction count")
)

transactions_over_time = transactions_over_time.rename(columns={"OnlyDate": "Date"})
st.write("Date range currently selected:")
st.write(start_date, "to", end_date)
st.write("Number of transactions used in this chart:")
st.write(len(filtered))

st.line_chart(
    transactions_over_time,
    x="Date",
    y="Transaction count"
)

st.subheader("Top 3 traded symbols")

top_symbols = (
    filtered
    .groupby("Symbol")
    .size()
    .reset_index(name="Transaction count")
)

top_symbols = top_symbols.sort_values(
    by="Transaction count",
    ascending=False
).head(3)

st.bar_chart(
    top_symbols,
    x="Symbol",
    y="Transaction count"
)

st.subheader("Top 5 sectors")

top_sectors = (
    filtered
    .groupby("sector")
    .size()
    .reset_index(name="Transaction count")
)

top_sectors = top_sectors.sort_values(
    by="Transaction count",
    ascending=False
).head(5)

st.bar_chart(
    top_sectors,
    x="sector",
    y="Transaction count"
)


st.subheader("Top 5 industries")

top_industries = (
    filtered
    .groupby("industry")
    .size()
    .reset_index(name="Transaction count")
)

top_industries = top_industries.sort_values(
    by="Transaction count",
    ascending=False
).head(5)

st.bar_chart(
    top_industries,
    x="industry",
    y="Transaction count"
)