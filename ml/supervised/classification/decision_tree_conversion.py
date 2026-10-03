"""
Decision Tree Classifier Baseline for Lead Conversion Prediction
Module: ml.supervised.classification.decision_tree_conversion
Target: target_is_converted (0 = Not Converted, 1 = Converted)
"""

from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)


def run_decision_tree_baseline() -> None:
    # 1. Define dataset paths
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    data_dir = project_root / "real_estate_intelligence_dataset" / "processed" / "ml_ready"
    
    train_path = data_dir / "track2_conversion_train.csv"
    test_path = data_dir / "track2_conversion_test.csv"

    # 2. Load ML-ready datasets
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    # 3. Separate features (X) and target (y)
    target_col = "target_is_converted"
    
    X_train = train_df.drop(columns=[target_col])
    y_train = train_df[target_col]

    X_test = test_df.drop(columns=[target_col])
    y_test = test_df[target_col]

    print("=" * 75)
    print("DECISION TREE CLASSIFIER BASELINE (LEAD CONVERSION)")
    print("=" * 75)
    print(f"X_train shape: {X_train.shape} | y_train shape: {y_train.shape}")
    print(f"X_test shape:  {X_test.shape}  | y_test shape:  {y_test.shape}")
    print(f"Predictor features count: {X_train.shape[1]}")

    # 4. Initialize and fit baseline Decision Tree model
    # Note: Clean baseline with random_state=42 (no hyperparameter tuning, no class weighting)
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    # 5. Generate predictions on test set
    y_pred = model.predict(X_test)

    # 6. Evaluation metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)

    print("\n" + "-" * 40)
    print("CLASSIFICATION PERFORMANCE METRICS")
    print("-" * 40)
    print(f"Accuracy:  {acc:.4f} ({acc * 100:.2f}%)")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1-Score:  {f1:.4f}")

    print("\nConfusion Matrix:")
    print(cm)
    print(f"  [TN={cm[0, 0]:>5d},  FP={cm[0, 1]:>5d}]")
    print(f"  [FN={cm[1, 0]:>5d},  TP={cm[1, 1]:>5d}]")

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Not Converted (0)", "Converted (1)"]))

    # 7. Prediction distribution vs Actual distribution
    pred_series = pd.Series(y_pred)
    print("-" * 40)
    print("PREDICTION DISTRIBUTION ANALYSIS")
    print("-" * 40)
    print("Actual Test Target Distribution:")
    print(y_test.value_counts())
    print(y_test.value_counts(normalize=True).round(4))

    print("\nPredicted Classes Distribution:")
    print(pred_series.value_counts())
    print(pred_series.value_counts(normalize=True).round(4))

    # 8. Feature Importances
    # Note: Feature importance reflects Gini impurity reduction across tree splits,
    # and must NOT be interpreted as causal influence.
    feature_names = X_train.columns.tolist()
    importances = model.feature_importances_
    
    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances
    }).sort_values("importance", ascending=False).reset_index(drop=True)

    print("\n" + "-" * 40)
    print("TOP 10 FEATURE IMPORTANCES (Gini Importance)")
    print("-" * 40)
    for idx, row in importance_df.head(10).iterrows():
        print(f"{idx + 1:02d}. {row['feature']:<30} : {row['importance']:.4f} ({row['importance'] * 100:.2f}%)")
    print("=" * 75)


if __name__ == "__main__":
    run_decision_tree_baseline()
