from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, average_precision_score

def analyze_thresholds_for_model(y_true, y_probs, thresholds=None):
    if thresholds is None:
        thresholds = np.arange(0.10, 0.95, 0.05)
        
    records = []
    for t in thresholds:
        preds = (y_probs >= t).astype(int)
        prec = precision_score(y_true, preds, zero_division=0)
        rec = recall_score(y_true, preds, zero_division=0)
        f1 = f1_score(y_true, preds, zero_division=0)
        pos_cnt = int(preds.sum())
        cm = confusion_matrix(y_true, preds)
        tn, fp, fn, tp = cm.ravel()
        
        records.append({
            "Threshold": round(t, 2),
            "Precision": prec,
            "Recall": rec,
            "F1": f1,
            "Pred_Positives": pos_cnt,
            "TN": tn,
            "FP": fp,
            "FN": fn,
            "TP": tp
        })
        
    return pd.DataFrame(records)

def run_classification_threshold_analysis():
    project_root = Path(__file__).resolve().parent.parent.parent
    train_path = project_root / "real_estate_intelligence_dataset" / "processed" / "ml_ready" / "track2_conversion_train.csv"
    
    df = pd.read_csv(train_path)
    target_col = "target_is_converted"
    
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    models = {
        "Random Forest Baseline": lambda: RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        "Logistic Regression Baseline (balanced)": lambda: LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42),
        "Tuned Logistic Regression (C=10.0, balanced)": lambda: LogisticRegression(C=10.0, class_weight="balanced", max_iter=1000, random_state=42)
    }
    
    oof_probs = {name: np.zeros(len(df), dtype=float) for name in models.keys()}
    
    for model_name, factory in models.items():
        for train_idx, val_idx in skf.split(X, y):
            X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
            X_val = X.iloc[val_idx]
            
            clf = factory()
            clf.fit(X_train, y_train)
            oof_probs[model_name][val_idx] = clf.predict_proba(X_val)[:, 1]
            
    print("=" * 100)
    print("CLASSIFICATION DECISION THRESHOLD ANALYSIS (5-FOLD OOF ON TRAINING DATA)")
    print("=" * 100)
    
    for model_name, probs in oof_probs.items():
        ap_score = average_precision_score(y, probs)
        thresh_df = analyze_thresholds_for_model(y.values, probs)
        
        best_row = thresh_df.loc[thresh_df["F1"].idxmax()]
        default_row = thresh_df.loc[thresh_df["Threshold"] == 0.50].iloc[0]
        
        print(f"\nModel: {model_name}")
        print(f"  Average Precision (PR-AUC): {ap_score:.4f}")
        print(f"  Default Threshold (0.50):    Precision={default_row['Precision']:.4f} | Recall={default_row['Recall']:.4f} | F1={default_row['F1']:.4f}")
        print(f"  Optimal F1 Threshold ({best_row['Threshold']:.2f}): Precision={best_row['Precision']:.4f} | Recall={best_row['Recall']:.4f} | F1={best_row['F1']:.4f}")
        print("-" * 100)
        print(thresh_df.round(4).to_string(index=False))
        print("-" * 100)

if __name__ == "__main__":
    run_classification_threshold_analysis()
