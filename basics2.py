import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option("display.max_columns", 100)
pd.set_option("display.width", 140)

plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.grid"] = False

df_raw = pd.read_csv('/Users/gregorko/Desktop/Archive/data/symbol_info_3-25.csv')


summary = pd.DataFrame({
    "column": df_raw.columns,
    "dtype": df_raw.dtypes.astype(str).values,
    "missing_values": df_raw.isna().sum().values,
    "missing_pct": (df_raw.isna().mean().values * 100).round(2)
})


df = df_raw.copy()
df = df[
    (df["is_etf"] == 0) &
    (df["is_fund"] == 0) &
    (df["is_actively_trading"] == 1) &
    (df["market_cap"] > 0) &
    (df["total_revenue"] > 0)
].copy()

df["market_cap_b"] = df["market_cap"] / 1e9
df["enterprise_value_b"] = df["enterprise_value"] / 1e9
df["revenue_b"] = df["total_revenue"] / 1e9
df["net_income_b"] = df["net_income"] / 1e9
df["free_cashflow_b"] = df["free_cashflow"] / 1e9


df["profit_margin_pct"] = df["profit_margins"] * 100
df["revenue_growth_pct"] = df["revenue_growth"] * 100
df["earnings_growth_pct"] = df["earnings_growth"] * 100
df["return_on_assets_pct"] = df["return_on_assets"] * 100
df["return_on_equity_pct"] = df["return_on_equity"] * 100

df["dividend_yield_pct"] = df["dividend_yield"]

df = df.replace([np.inf, -np.inf], np.nan)

print("Cleaned investment universe:", df.shape)
print(df[["symbol", "company_name", "sector", "market_cap_b", "revenue_b", "profit_margin_pct", "beta"]].head())

def billions_formatter(x, pos):
    return f"{x:,.0f}B"

def pct_formatter(x, pos):
    return f"{x:.0f}%"

def clean_spines(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return ax

def annotate_hbar(ax, fmt="{:.1f}"):
    for patch in ax.patches:
        width = patch.get_width()
        y = patch.get_y() + patch.get_height() / 2
        ax.text(width, y, "  " + fmt.format(width), va="center", fontsize=9)

plt.figure(figsize=(10, 5))
plt.hist(df["market_cap_b"].dropna(), bins=50)
plt.title("Distribution of Market Capitalization")
plt.xlabel("Market capitalization, USD billions")
plt.ylabel("Number of companies")

market_cap = df["market_cap_b"].dropna()

fig, ax = plt.subplots(figsize=(11, 5))

ax.hist(

    market_cap,          # Data to plot: one numerical value per company.
                         # In this case, market_cap contains the market capitalization values.

    bins=60,             # Number of intervals used to split the data.
                         # More bins = more detail, but the chart may become noisy.
                         # Fewer bins = smoother chart, but less detail.

    color="#4C78A8",     # Fill color of the bars.
                         # Hexadecimal color code.
                         # This blue is visually clean and works well in business charts.

    edgecolor="white",   # Color of the border around each bar.
                         # White edges help separate adjacent bars visually.

    alpha=0.85           # Transparency level of the bars.
                         # 1.0 means fully opaque.
                         # 0.0 means fully transparent.
                         # 0.85 keeps the color strong but slightly softer.
)

median_value = market_cap.median()
mean_value = market_cap.mean()

ax.axvline(median_value, color="#F58528", linestyle="--", linewidth=2, label=f"Median: {median_value:,.1f}B")
ax.axvline(mean_value, color="#E45754", linestyle=":", linewidth=2.5, label=f"Mean: {mean_value:,.1f}B")

ax.set_title("Market capitalization is highly skewed: a few giants dominate")
ax.set_xlabel("Market capitalization, USD v biliónoch")
ax.set_ylabel("Počet firiem")
ax.grid(axis="y", alpha=0.25)
ax.legend()
clean_spines(ax)

plt.show()