import pandas as pd

df = pd.read_csv("SalesAnalyticsAPI/data/FMCG_2022_2024.csv")

# print("\nFirst 5 rows")
# print(df.head())

# print("\nColumns")
# regional_options = df["region"].value_counts()
# print(regional_options)

print(df["category"].value_counts())

# print("\nData Types")
# print(df.dtypes)

# print("\nMissing Values")
# print(df.isnull().sum())

# print("\nShape")
# print(df.shape)



# print("\nSample Values")
# for col in df.columns:
#     print(f"\n{col}")
#     print(df[col].unique()[:10])