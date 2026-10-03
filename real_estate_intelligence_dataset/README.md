# Real Estate Intelligence & AI Decision Engine Dataset

Synthetic Analytics, Business Intelligence & Machine Learning Dataset (2024-01-01 to 2026-09-30).

## Architecture & Relational Schema
```text
projects (20)
   ├── units (5,000)
   │     ├── listings (18,000)
   │     │     └── leads (60,000)
   │     │           └── viewings (40,000)
   │     │                 └── deals (12,000)
   │     ├── leases (3,200)
   │     │     └── rent_payments (32,000)
   │     └── maintenance (12,000)
   └── expenses (24,000)

customers (10,000) ──> leads & tenants (2,500)
agents (100) ──> listings, leads, viewings, deals
```

## Directory Structure
```text
real_estate_intelligence_dataset/
├── raw/
│   ├── projects.csv
│   ├── units.csv
│   ├── customers.csv
│   ├── agents.csv
│   ├── listings.csv
│   ├── leads.csv
│   ├── viewings.csv
│   ├── deals.csv
│   ├── expenses.csv
│   ├── tenants.csv
│   ├── leases.csv
│   ├── rent_payments.csv
│   └── maintenance.csv
├── reports/
│   ├── validation_report.csv
│   ├── data_quality_report.csv
│   └── data_summary.json
├── data_dictionary.csv
├── manifest.csv
└── README.md
```

## Highlights & Validation
- **Seed**: 42 (Deterministic generation)
- **Currency**: EGP (Synthetic values)
- **Critical Validation Checks Passed**: 47/47 (100% Referential & Chronological Integrity)
- **Controlled Data Quality**: ~95%+ clean data with realistic missingness and labeled anomalies for robust ML training.
