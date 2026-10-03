"""
Random Forest Classifier Baseline for Lead Conversion Prediction
Module: ml.supervised.classification.random_forest_conversion
Target: target_is_converted (0 = Not Converted, 1 = Converted)
"""

from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)


def run_random_forest_baseline() -> None:
    # 1. Define dataset paths
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    data_dir = project_root / "real_estate_intelligence_dataset" / "processed" / "ml_ready"
    
    train_path = data_dir / "track2_conversion_train.csv"
    test_path = data_dir / "track2_conversion_test.csv"

    # Validation: Assert file existence
    assert train_path.exists(), f"Train dataset missing: {train_path}"
    assert test_path.exists(), f"Test dataset missing: {test_path}"

    # 2. Load ML-ready datasets
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    # 3. Separate features (X) and target (y)
    target_col = "target_is_converted"
    assert target_col in train_df.columns, f"Target column '{target_col}' missing in train set"
    assert target_col in test_df.columns, f"Target column '{target_col}' missing in test set"
    
    X_train = train_df.drop(columns=[target_col])
    y_train = train_df[target_col]

    X_test = test_df.drop(columns=[target_col])
    y_test = test_df[target_col]

    # Sanity checks on dimensions and data integrity
    assert X_train.shape[1] == X_test.shape[1] == 27, "Feature column count mismatch!"
    assert target_col not in X_train.columns, "Target leakage detected in X_train!"
    assert target_col not in X_test.columns, "Target leakage detected in X_test!"
    assert X_train.isna().sum().sum() == 0, "NaN values detected in X_train!"
    assert X_test.isna().sum().sum() == 0, "NaN values detected in X_test!"
    assert set(y_train.unique()).issubset({0, 1}), "Unexpected classes in y_train!"
    assert set(y_test.unique()).issubset({0, 1}), "Unexpected classes in y_test!"

    print("=" * 75)
    print("RANDOM FOREST CLASSIFIER BASELINE (LEAD CONVERSION)")
    print("=" * 75)
    print(f"X_train shape: {X_train.shape} | y_train shape: {y_train.shape}")
    print(f"X_test shape:  {X_test.shape}  | y_test shape:  {y_test.shape}")
    print(f"Predictor features count: {X_train.shape[1]}")

    # 4. Initialize and fit baseline Random Forest model
    # Baseline configuration: n_estimators=100, random_state=42, n_jobs=-1
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # 5. Generate predictions and class probabilities on test set
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    assert len(y_pred) == len(y_test), "Prediction length mismatch!"
    assert set(y_pred).issubset({0, 1}), "Predictions contain invalid classes!"

    # 6. Evaluation metrics (focusing on positive class 1 = Converted)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)

    print("\n" + "-" * 40)
    print("CLASSIFICATION PERFORMANCE METRICS")
    print("-" * 40)
    print(f"Accuracy:  {acc:.4f} ({acc * 100:.2f}%)")
    print(f"Precision (Class 1 = Converted): {prec:.4f}")
    print(f"Recall    (Class 1 = Converted): {rec:.4f}")
    print(f"F1-Score  (Class 1 = Converted): {f1:.4f}")

    print("\nConfusion Matrix:")
    print(cm)
    print(f"  [TN={cm[0, 0]:>5d},  FP={cm[0, 1]:>5d}]")
    print(f"  [FN={cm[1, 0]:>5d},  TP={cm[1, 1]:>5d}]")

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Not Converted (0)", "Converted (1)"]))

    # 7. Probability analysis
    print("-" * 40)
    print("PROBABILITY DISTRIBUTION ANALYSIS")
    print("-" * 40)
    print(f"Min probability:  {y_prob.min():.4f}")
    print(f"Max probability:  {y_prob.max():.4f}")
    print(f"Mean probability: {y_prob.mean():.4f}")

    # 8. Prediction distribution vs Actual distribution
    pred_series = pd.Series(y_pred)
    print("\n" + "-" * 40)
    print("PREDICTION DISTRIBUTION ANALYSIS")
    print("-" * 40)
    print("Actual Test Target Distribution:")
    print(y_test.value_counts())
    print(y_test.value_counts(normalize=True).round(4))

    print("\nPredicted Classes Distribution:")
    print(pred_series.value_counts())
    print(pred_series.value_counts(normalize=True).round(4))

    # 9. Feature Importances
    # Note: Feature importance values represent Gini impurity reduction across all 100 trees,
    # and should NOT be interpreted as causal effects.
    feature_names = X_train.columns.tolist()
    importances = model.feature_importances_
    assert len(importances) == len(feature_names) == 27, "Feature importances count mismatch!"
    
    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances
    }).sort_values("importance", ascending=False).reset_index(drop=True)

    print("\n" + "-" * 40)
    print("ALL 27 FEATURE IMPORTANCES (Gini Importance)")
    print("-" * 40)
    for idx, row in importance_df.iterrows():
        print(f"{idx + 1:02d}. {row['feature']:<32} : {row['importance']:.4f} ({row['importance'] * 100:.2f}%)")
    print("=" * 75)


if __name__ == "__main__":
    run_random_forest_baseline()
