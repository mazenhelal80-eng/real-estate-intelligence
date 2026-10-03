import pandas as pd

comparison_data = [
    {
        "Model": "Naive (Last Value)",
        "Type": "Deterministic Baseline",
        "Temporal Mechanism": "Point lag persistence (y_hat_t = y_t-1)",
        "Computational Cost": "Zero training, instant lookup",
        "Out-of-sample Mode": "One-step rolling",
        "Key Assumption": "Previous day observation is the best point estimate"
    },
    {
        "Model": "Seasonal Naive (7-Day)",
        "Type": "Deterministic Baseline",
        "Temporal Mechanism": "7-day seasonal lag (y_hat_t = y_t-7)",
        "Computational Cost": "Zero training, instant lookup",
        "Out-of-sample Mode": "One-step rolling",
        "Key Assumption": "Strict weekly recurring day-of-week seasonality"
    },
    {
        "Model": "Moving Average (7-Day)",
        "Type": "Statistical Baseline",
        "Temporal Mechanism": "Unweighted average of past 7 days (shift(1).rolling(7))",
        "Computational Cost": "Minimal rolling sum computation",
        "Out-of-sample Mode": "One-step rolling",
        "Key Assumption": "Short-term local mean reversion with noise smoothing"
    },
    {
        "Model": "Linear Regression",
        "Type": "Parametric Linear ML",
        "Temporal Mechanism": "Linear combination of autoregressive lags and calendar indicators",
        "Computational Cost": "Closed-form OLS fit (O(p^2 n))",
        "Out-of-sample Mode": "One-step rolling feature prediction",
        "Key Assumption": "Linear relationship between lagged history and future net cash flow"
    },
    {
        "Model": "Random Forest Regressor",
        "Type": "Non-linear Ensemble ML",
        "Temporal Mechanism": "Ensemble decision trees over lags, rolling stats, and calendar features",
        "Computational Cost": "Moderate parallelized tree induction",
        "Out-of-sample Mode": "One-step rolling feature prediction",
        "Key Assumption": "Complex non-linear interactions between rolling volatility and calendar cycles"
    },
    {
        "Model": "HistGradientBoosting",
        "Type": "Gradient Boosted Trees ML",
        "Temporal Mechanism": "Sequential gradient descent boosting over binned temporal features",
        "Computational Cost": "Fast histogram-based gradient boosting",
        "Out-of-sample Mode": "One-step rolling feature prediction",
        "Key Assumption": "Non-linear additive residuals with robust tree regularization"
    }
]

df_comp = pd.DataFrame(comparison_data)

print("=" * 105)
print("TIME SERIES FORECASTING METHODS - FACTUAL COMPARISON")
print("=" * 105)
for idx, row in df_comp.iterrows():
    print(f"\nModel: {row['Model']}")
    print(f"  Type:                {row['Type']}")
    print(f"  Temporal Mechanism:  {row['Temporal Mechanism']}")
    print(f"  Computational Cost:  {row['Computational Cost']}")
    print(f"  Out-of-sample Mode:  {row['Out-of-sample Mode']}")
    print(f"  Key Assumption:      {row['Key Assumption']}")

print("=" * 105)
