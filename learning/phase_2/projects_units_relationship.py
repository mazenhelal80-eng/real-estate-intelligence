import pandas as pd

df_projects = pd.read_csv(r"D:\Desktop\real-estate-intelligence\real_estate_intelligence_dataset\raw\projects.csv")
df_units = pd.read_csv(r"D:\Desktop\real-estate-intelligence\real_estate_intelligence_dataset\raw\units.csv")

df_merged = pd.merge(df_projects,df_units,on="project_id")
print(df_merged.head())
print(df_merged.info())
print(df_merged.isnull().sum())
print("------------------------------------------------------------")
print(df_merged.groupby("developer_name")["project_id"].count().sort_values(ascending=False))
avrege_price=df_merged.groupby("developer_name")["base_price_egp"].mean()
top_avrege=avrege_price.idxmax()
top_avrege_val=avrege_price.max()
print("top avrege price developer",top_avrege,"with avrege price",top_avrege_val)
df_merged.groupby("developer_name")["area_sqm"].mean()
df_merged.groupby("developer_name")["base_price_egp"].mean()
print("average price by developer",df_merged.groupby("developer_name")["base_price_egp"].mean())
print("average area by developer",df_merged.groupby("developer_name")["area_sqm"].mean())