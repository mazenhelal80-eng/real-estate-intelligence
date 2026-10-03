from pathlib import Path
import itertools
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

def evaluate_cv_config(clf_factory, X, y, skf):
    fold_f1s = []
    fold_precs = []
    fold_recs = []
    fold_accs = []
    
    for train_idx, val_idx in skf.split(X, y):
        X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
        X_val, y_val = X.iloc[val_idx], y.iloc[val_idx]
        
        clf = clf_factory()
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_val)
        
        fold_f1s.append(f1_score(y_val, y_pred, zero_division=0))
        fold_precs.append(precision_score(y_val, y_pred, zero_division=0))
        fold_recs.append(recall_score(y_val, y_pred, zero_division=0))
        fold_accs.append(accuracy_score(y_val, y_pred))
        
    return {
        "F1_mean": np.mean(fold_f1s),
        "F1_std": np.std(fold_f1s),
        "Precision_mean": np.mean(fold_precs),
        "Recall_mean": np.mean(fold_recs),
        "Accuracy_mean": np.mean(fold_accs)
    }

def run_classification_tuning():
    project_root = Path(__file__).resolve().parent.parent.parent
    train_path = project_root / "real_estate_intelligence_dataset" / "processed" / "ml_ready" / "track2_conversion_train.csv"
    
    df = pd.read_csv(train_path)
    target_col = "target_is_converted"
    
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    print("=" * 95)
    print("HYPERPARAMETER TUNING (5-FOLD STRATIFIED CV ON TRAINING DATA)")
    print("=" * 95)
    
    lr_grid = {
        "C": [0.01, 0.1, 1.0, 10.0],
        "class_weight": [None, "balanced"]
    }
    lr_results = []
    for params in [dict(zip(lr_grid.keys(), v)) for v in itertools.product(*lr_grid.values())]:
        factory = lambda p=params: LogisticRegression(C=p["C"], class_weight=p["class_weight"], max_iter=1000, random_state=42)
        metrics = evaluate_cv_config(factory, X, y, skf)
        lr_results.append({**params, **metrics})
    
    lr_df = pd.DataFrame(lr_results).sort_values("F1_mean", ascending=False)
    print("\n1. Logistic Regression Tuning Results (Top 4 Configurations):")
    print(lr_df.head(4).round(4).to_string(index=False))
    
    dt_grid = {
        "max_depth": [5, 10, 15, None],
        "min_samples_leaf": [1, 5, 20],
        "class_weight": [None, "balanced"]
    }
    dt_results = []
    for params in [dict(zip(dt_grid.keys(), v)) for v in itertools.product(*dt_grid.values())]:
        factory = lambda p=params: DecisionTreeClassifier(max_depth=p["max_depth"], min_samples_leaf=p["min_samples_leaf"], class_weight=p["class_weight"], random_state=42)
        metrics = evaluate_cv_config(factory, X, y, skf)
        dt_results.append({**params, **metrics})
        
    dt_df = pd.DataFrame(dt_results).sort_values("F1_mean", ascending=False)
    print("\n2. Decision Tree Tuning Results (Top 4 Configurations):")
    print(dt_df.head(4).round(4).to_string(index=False))
    
    rf_grid = {
        "n_estimators": [50, 100],
        "max_depth": [10, 20, None],
        "min_samples_leaf": [1, 5],
        "class_weight": [None, "balanced"]
    }
    rf_results = []
    for params in [dict(zip(rf_grid.keys(), v)) for v in itertools.product(*rf_grid.values())]:
        factory = lambda p=params: RandomForestClassifier(n_estimators=p["n_estimators"], max_depth=p["max_depth"], min_samples_leaf=p["min_samples_leaf"], class_weight=p["class_weight"], random_state=42, n_jobs=-1)
        metrics = evaluate_cv_config(factory, X, y, skf)
        rf_results.append({**params, **metrics})
        
    rf_df = pd.DataFrame(rf_results).sort_values("F1_mean", ascending=False)
    print("\n3. Random Forest Tuning Results (Top 4 Configurations):")
    print(rf_df.head(4).round(4).to_string(index=False))
    print("=" * 95)
    
    best_overall = rf_df.iloc[0]
    print(f"\nBest Development Candidate: Random Forest (F1={best_overall['F1_mean']:.4f})")
    print(f"Parameters: n_estimators={best_overall['n_estimators']}, max_depth={best_overall['max_depth']}, min_samples_leaf={best_overall['min_samples_leaf']}, class_weight={best_overall['class_weight']}")

if __name__ == "__main__":
    run_classification_tuning()
