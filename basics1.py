import pandas as pd

df = pd.read_csv('/Users/gregorko/Desktop/Archive/data/symbol_info_3-25.csv')


sample = df.sample(n=15, random_state=42)
df_sample = sample[['symbol', 'market_cap', 'sector']]
print(df_sample)