import pandas as pd

df = pd.read_csv(
    r"D:\Desktop\real-estate-intelligence\real_estate_intelligence_dataset\raw\units.csv"
)
referense_year=2026
df["property_age"]=referense_year-df["construction_year"]
print(df.head())
print(df["property_age"].min())
print(df["property_age"].max())
print(df["property_age"].value_counts().sort_index())