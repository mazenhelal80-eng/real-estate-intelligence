import pandas as pd 
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, r2_score,mean_squared_error




train_df=pd.read_csv(r"D:\Desktop\real-estate-intelligence\real_estate_intelligence_dataset\processed\ml_ready\track1_pricing_train.csv")
test_df=pd.read_csv(r"D:\Desktop\real-estate-intelligence\real_estate_intelligence_dataset\processed\ml_ready\track1_pricing_test.csv")
print("Train Head:",train_df.head())
print("Train Info:",train_df.info())
print("Test Head:",test_df.head())
print("Test Info:",test_df.info())
#---------------------------------------------
y=train_df["target_base_price_egp"]
X=train_df.drop("target_base_price_egp", axis=1)
print("Features Shape:", X.shape)
print("Feature Names:", X.columns.tolist())
print("Target Shape:", y.shape)
print("--------------------------------------------------------------------------")

X_train=train_df.drop("target_base_price_egp", axis=1)
y_train=train_df["target_base_price_egp"]
X_test=test_df.drop("target_base_price_egp", axis=1)
y_test=test_df["target_base_price_egp"]
print("X_train Shape:", X_train.shape)
print("y_train Shape:", y_train.shape)
print("X_test Shape:", X_test.shape)
print("y_test Shape:", y_test.shape)
print("--------------------------------------------------------------------------")
model=DecisionTreeRegressor(random_state=42,max_depth=10)
model.fit(X_train, y_train)

y_pred=model.predict(X_test)
print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))




comparison = pd.DataFrame({
    "actual_price": y_test,
    "predicted_price": y_pred
})

print(comparison.head(10))

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(f"Evaluation Metrics:\nMAE: {mae:.2f}\nR2: {r2:.2f}\nMSE: {mse:.2f}")

comparison['error_absolute']=abs(comparison['actual_price']-comparison['predicted_price'])
print("error mean",comparison["error_absolute"].mean())
print(comparison.head(10))

print(comparison.sort_values("error_absolute", ascending=False).head(10))


comparison['error_percentage']=abs((comparison['predicted_price']-comparison['actual_price']))/comparison['actual_price']*100
print("error percentage mean",comparison["error_percentage"].mean())
print(comparison.head(10),"#---------------error percentage mean---------------#")
print(comparison.sort_values("error_percentage", ascending=False).head(10),"#---------------error percentage top 10---------------#")
print((y_pred < 0).sum())
print(comparison["error_percentage"].describe())
print("-------------------------")
model.feature_importances_
pd.Series(model.feature_importances_,index=X.columns)
print(pd.Series(model.feature_importances_,index=X.columns).sort_values(ascending=False))