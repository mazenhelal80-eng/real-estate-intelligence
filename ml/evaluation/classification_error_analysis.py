from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score

def run_classification_error_analysis():
    project_root = Path(__file__).resolve().parent.parent.parent
    train_path = project_root / "real_estate_intelligence_dataset" / "processed" / "ml_ready" / "track2_conversion_train.csv"
    
    df = pd.read_csv(train_path)
    target_col = "target_is_converted"
    
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    models = {
        "Logistic Regression (balanced)": lambda: LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42),
        "Decision Tree": lambda: DecisionTreeClassifier(random_state=42),
        "Random Forest": lambda: RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    }
    
    oof_preds = {name: np.zeros(len(df), dtype=int) for name in models.keys()}
    oof_probs = {name: np.zeros(len(df), dtype=float) for name in models.keys()}
    
    for model_name, factory in models.items():
        for train_idx, val_idx in skf.split(X, y):
            X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
            X_val = X.iloc[val_idx]
            
            clf = factory()
            clf.fit(X_train, y_train)
            
            oof_preds[model_name][val_idx] = clf.predict(X_val)
            oof_probs[model_name][val_idx] = clf.predict_proba(X_val)[:, 1]
            
    print("=" * 90)
    print("CLASSIFICATION ERROR ANALYSIS (5-FOLD OUT-OF-FOLD VALIDATION ON TRAIN SET)")
    print("=" * 90)
    print(f"Total Training Samples: {len(df):,d} (Class 0: {(y == 0).sum():,d}, Class 1: {(y == 1).sum():,d})")
    print("-" * 90)
    
    for model_name in models.keys():
        preds = oof_preds[model_name]
        probs = oof_probs[model_name]
        cm = confusion_matrix(y, preds)
        tn, fp, fn, tp = cm.ravel()
        
        prec = precision_score(y, preds, zero_division=0)
        rec = recall_score(y, preds, zero_division=0)
        f1 = f1_score(y, preds, zero_division=0)
        
        print(f"\nModel: {model_name}")
        print(f"  Confusion Matrix: TN={tn:,d} | FP={fp:,d} | FN={fn:,d} | TP={tp:,d}")
        print(f"  Precision: {prec:.4f} | Recall: {rec:.4f} | F1: {f1:.4f}")
        print(f"  False Positive Rate: {fp / (tn + fp):.4f} ({fp:,d} non-converted leads misclassified as converted)")
        print(f"  False Negative Rate: {fn / (fn + tp):.4f} ({fn:,d} converted leads missed by model)")
        
        analysis_df = df.copy()
        analysis_df["actual"] = y
        analysis_df["pred"] = preds
        analysis_df["prob"] = probs
        
        fp_subset = analysis_df[(analysis_df["actual"] == 0) & (analysis_df["pred"] == 1)]
        fn_subset = analysis_df[(analysis_df["actual"] == 1) & (analysis_df["pred"] == 0)]
        tp_subset = analysis_df[(analysis_df["actual"] == 1) & (analysis_df["pred"] == 1)]
        tn_subset = analysis_df[(analysis_df["actual"] == 0) & (analysis_df["pred"] == 0)]
        
        print(f"\n  Mean Numerical Characteristics Across Error Subsets ({model_name}):")
        metrics_comp = pd.DataFrame({
            "TN (True Neg)": tn_subset[["lead_score", "interaction_count", "monthly_income_egp", "budget_max_egp", "prob"]].mean(),
            "FP (False Pos)": fp_subset[["lead_score", "interaction_count", "monthly_income_egp", "budget_max_egp", "prob"]].mean(),
            "FN (False Neg)": fn_subset[["lead_score", "interaction_count", "monthly_income_egp", "budget_max_egp", "prob"]].mean(),
            "TP (True Pos)": tp_subset[["lead_score", "interaction_count", "monthly_income_egp", "budget_max_egp", "prob"]].mean()
        })
        print(metrics_comp.round(2).to_string())
        
        lead_sources = [c for c in df.columns if c.startswith("lead_source_")]
        source_fp = fp_subset[lead_sources].sum().rename("FP_count")
        source_fn = fn_subset[lead_sources].sum().rename("FN_count")
        source_summary = pd.concat([source_fp, source_fn], axis=1).sort_values("FP_count", ascending=False)
        
        print(f"\n  Error Distribution by Lead Source:")
        print(source_summary.head(4).to_string())
        print("-" * 90)

if __name__ == "__main__":
    run_classification_error_analysis()
