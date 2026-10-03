"""
Phase 5: Classification Baseline Models Cross-Validated Evaluation
Module: ml.evaluation.classification_model_evaluation
Purpose: Explicit 5-fold cross-validated evaluation and descriptive comparison
         across the three baseline models: Logistic Regression, Decision Tree, Random Forest.
"""

from pathlib import Path
from typing import Dict, List, Callable
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


def evaluate_models_cross_validation() -> None:
    # 1. Define dataset path (Training set only)
    project_root = Path(__file__).resolve().parent.parent.parent
    train_path = (
        project_root
        / "real_estate_intelligence_dataset"
        / "processed"
        / "ml_ready"
        / "track2_conversion_train.csv"
    )

    assert train_path.exists(), f"Training dataset missing at: {train_path}"

    # 2. Load dataset
    train_df = pd.read_csv(train_path)
    target_col = "target_is_converted"
    assert target_col in train_df.columns, f"Target column '{target_col}' missing!"

    X = train_df.drop(columns=[target_col])
    y = train_df[target_col]

    # Data validation checks
    assert X.shape[1] == 27, f"Expected 27 features, got {X.shape[1]}"
    assert target_col not in X.columns, "Target leakage in X!"
    assert X.isna().sum().sum() == 0, "NaN values detected in X!"
    assert np.all(np.isfinite(X.values)), "Infinite values detected in X!"
    assert set(y.unique()).issubset({0, 1}), "Target contains non-binary values!"

    total_samples = len(train_df)
    pos_count = int((y == 1).sum())
    neg_count = int((y == 0).sum())

    print("=" * 80)
    print("PHASE 5: 5-FOLD STRATIFIED CV EVALUATION ACROSS CLASSIFICATION BASELINES")
    print("=" * 80)
    print(f"Training Dataset: track2_conversion_train.csv ({total_samples:,d} rows, {X.shape[1]} features)")
    print(f"Target Distribution: Class 0 = {neg_count:,d} ({neg_count/total_samples*100:.2f}%) | Class 1 = {pos_count:,d} ({pos_count/total_samples*100:.2f}%)")
    print("=" * 80)

    # 3. Define 5-Fold Stratified Cross Validation Strategy
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # 4. Model Factory definitions (Fresh instance created per fold)
    # Model 1: Logistic Regression (class_weight='balanced') matching lead_conversion.py baseline
    # Model 2: Decision Tree (random_state=42) matching decision_tree_conversion.py baseline
    # Model 3: Random Forest (n_estimators=100, random_state=42, n_jobs=-1) matching random_forest_conversion.py baseline
    model_factories: Dict[str, Callable[[], object]] = {
        "Logistic Regression (balanced)": lambda: LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42),
        "Decision Tree": lambda: DecisionTreeClassifier(random_state=42),
        "Random Forest": lambda: RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    }

    all_model_results = []
    comparison_summary_rows = []

    # 5. Explicit evaluation loop per model across all folds
    for model_name, model_factory in model_factories.items():
        print(f"\n==================================================")
        print(f"MODEL: {model_name}")
        print(f"==================================================")

        fold_accuracies = []
        fold_precisions = []
        fold_recalls = []
        fold_f1s = []
        fold_tns = []
        fold_fps = []
        fold_fns = []
        fold_tps = []

        oof_predictions = np.zeros(total_samples, dtype=int)
        validated_indices = []

        for fold_idx, (train_idx, val_idx) in enumerate(skf.split(X, y), 1):
            # Assert no overlap
            assert len(set(train_idx).intersection(set(val_idx))) == 0, f"Leakage in fold {fold_idx}"
            validated_indices.extend(val_idx)

            X_train_fold, y_train_fold = X.iloc[train_idx], y.iloc[train_idx]
            X_val_fold, y_val_fold = X.iloc[val_idx], y.iloc[val_idx]

            # Recreate fresh model instance for this fold
            model = model_factory()
            model.fit(X_train_fold, y_train_fold)

            y_pred_fold = model.predict(X_val_fold)
            assert len(y_pred_fold) == len(y_val_fold)
            assert set(y_pred_fold).issubset({0, 1})

            oof_predictions[val_idx] = y_pred_fold

            acc = accuracy_score(y_val_fold, y_pred_fold)
            prec = precision_score(y_val_fold, y_pred_fold, zero_division=0)
            rec = recall_score(y_val_fold, y_pred_fold, zero_division=0)
            f1 = f1_score(y_val_fold, y_pred_fold, zero_division=0)
            cm = confusion_matrix(y_val_fold, y_pred_fold, labels=[0, 1])

            tn, fp, fn, tp = cm.ravel()

            fold_accuracies.append(acc)
            fold_precisions.append(prec)
            fold_recalls.append(rec)
            fold_f1s.append(f1)
            fold_tns.append(tn)
            fold_fps.append(fp)
            fold_fns.append(fn)
            fold_tps.append(tp)

            print(f"\nFold {fold_idx}")
            print(f"Accuracy:  {acc:.4f} ({acc*100:.2f}%)")
            print(f"Precision: {prec:.4f}")
            print(f"Recall:    {rec:.4f}")
            print(f"F1:        {f1:.4f}")
            print(f"TN: {tn:>5d} | FP: {fp:>5d}")
            print(f"FN: {fn:>5d} | TP: {tp:>5d}")

        # Summary statistics across 5 folds
        acc_mean, acc_std = np.mean(fold_accuracies), np.std(fold_accuracies)
        prec_mean, prec_std = np.mean(fold_precisions), np.std(fold_precisions)
        rec_mean, rec_std = np.mean(fold_recalls), np.std(fold_recalls)
        f1_mean, f1_std = np.mean(fold_f1s), np.std(fold_f1s)

        mean_tn, mean_fp = np.mean(fold_tns), np.mean(fold_fps)
        mean_fn, mean_tp = np.mean(fold_fns), np.mean(fold_tps)

        # Aggregated out-of-fold confusion matrix
        total_cm = confusion_matrix(y, oof_predictions, labels=[0, 1])
        tot_tn, tot_fp, tot_fn, tot_tp = total_cm.ravel()

        print(f"\n--------------------------------------------------")
        print(f"Cross Validation Summary ({model_name})")
        print(f"--------------------------------------------------")
        print(f"Accuracy:  Mean: {acc_mean:.4f}  | Std: {acc_std:.4f}")
        print(f"Precision: Mean: {prec_mean:.4f}  | Std: {prec_std:.4f}")
        print(f"Recall:    Mean: {rec_mean:.4f}  | Std: {rec_std:.4f}")
        print(f"F1:        Mean: {f1_mean:.4f}  | Std: {f1_std:.4f}")
        print(f"\nMean Confusion Metrics Per Fold:")
        print(f"Mean TN: {mean_tn:>7.1f} | Mean FP: {mean_fp:>7.1f}")
        print(f"Mean FN: {mean_fn:>7.1f} | Mean TP: {mean_tp:>7.1f}")
        print(f"\nTotal Aggregated Confusion Matrix (All {total_samples:,d} OOF Validation Predictions):")
        print(f"[[{tot_tn:>6d}, {tot_fp:>6d}],")
        print(f" [{tot_fn:>6d}, {tot_tp:>6d}]]")
        print(f"  [Total TN = {tot_tn:,d},  Total FP = {tot_fp:,d}]")
        print(f"  [Total FN = {tot_fn:,d},  Total TP = {tot_tp:,d}]")

        comparison_summary_rows.append({
            "Model": model_name,
            "Accuracy Mean": f"{acc_mean:.4f}",
            "Accuracy Std": f"{acc_std:.4f}",
            "Precision Mean": f"{prec_mean:.4f}",
            "Precision Std": f"{prec_std:.4f}",
            "Recall Mean": f"{rec_mean:.4f}",
            "Recall Std": f"{rec_std:.4f}",
            "F1 Mean": f"{f1_mean:.4f}",
            "F1 Std": f"{f1_std:.4f}",
        })

    # 6. Print Final Descriptive Comparison Table
    print("\n" + "=" * 80)
    print("DESCRIPTIVE CROSS-VALIDATION COMPARISON TABLE")
    print("=" * 80)
    comp_df = pd.DataFrame(comparison_summary_rows)
    print(comp_df.to_string(index=False))
    print("=" * 80)


if __name__ == "__main__":
    evaluate_models_cross_validation()
