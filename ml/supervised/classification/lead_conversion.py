import pandas as pd 
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
from sklearn.metrics import f1_score





train_df = pd.read_csv(
    r"D:\Desktop\real-estate-intelligence\real_estate_intelligence_dataset\processed\ml_ready\track2_conversion_train.csv"
)

test_df = pd.read_csv(
    r"D:\Desktop\real-estate-intelligence\real_estate_intelligence_dataset\processed\ml_ready\track2_conversion_test.csv"
)


X_train = train_df.drop("target_is_converted", axis=1)
y_train = train_df["target_is_converted"]

X_test = test_df.drop("target_is_converted", axis=1)
y_test = test_df["target_is_converted"]

model = LogisticRegression(class_weight="balanced")
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# Target distribution
print("\nTest target distribution:")
print(y_test.value_counts())
print(y_test.value_counts(normalize=True))


# Prediction probabilities
y_prob = model.predict_proba(X_test)[:, 1]

print("\nProbability Analysis:")
print("Min probability:", y_prob.min())
print("Max probability:", y_prob.max())
print("Mean probability:", y_prob.mean())

print("\nFirst 20 probabilities:")
print(y_prob[:20])


print("F1:", f1_score(y_test, y_pred))