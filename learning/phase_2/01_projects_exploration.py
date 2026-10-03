import pandas as pd

df=pd.read_csv(r"D:\Desktop\real-estate-intelligence\real_estate_intelligence_dataset\raw\projects.csv")
print(df.head())
print("Columns:",df.columns)
print("\nInfo")
df.info()
print("\nshape",df.shape)
print("is null",df.isnull().sum())
print("is duplicate",df.duplicated().sum())
#------------------------------------------------------------
print(df.groupby("developer_name")["project_id"].count().sort_values(ascending=False))
print("------------------------------------------------------------")
print(df.groupby("location")["project_id"].count().sort_values(ascending=False))

df["launch_date"]=pd.to_datetime(df["launch_date"])
df["expected_completion_date"]=pd.to_datetime(df["expected_completion_date"])
df["duration"]=df["expected_completion_date"]-df["launch_date"]
print(df)

#------------------------------------------------------------
