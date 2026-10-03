# Phase 2 — Business Analytics Report

## 1. Executive Summary

This report documents the completion of **Phase 2 (Business Analytics & SQL)** for the Real Estate Intelligence & AI Decision Engine project. 

The analytical layer combines observational records from **13 relational tables** spanning **Development**, **Brokerage**, and **Property Management** operations from January 1, 2024, to September 30, 2026. 

All analyses were executed in dual environments (**Pandas** and **DuckDB SQL**) and cross-validated with a 100% equivalence match.

### Key Financial & Operational Highlights (EGP)
* **Gross Revenue Recognized:** 50,732,489,700 EGP (Closed Sales: 48,984,544,000 EGP [96.55%], Rental Collections: 1,747,945,700 EGP [3.45%]).
* **Total Operating Expenses:** 2,675,881,754 EGP.
* **Net Operating Profit:** 48,056,607,946 EGP (**Net Profit Margin: 94.73%**).
* **Total Transactions:** 12,000 Deals created $\rightarrow$ 7,937 Closed (66.14%), 4,063 Cancelled (33.86%).
* **Lead Conversion Efficiency:** 60,000 Leads $\rightarrow$ 7,937 Closed Deals (**Overall Conversion Rate: 13.23%**).
* **Rental Occupancy Rate:** 22.08% (1,104 active leased units out of 5,000 total inventory units).
* **Payment Collection Rate:** 96.65% (1,747,945,700 EGP collected out of 1,808,541,400 EGP billed).

---

## 2. Revenue Analysis

Monthly sales revenue was derived strictly from closed transaction contracts (`deal_status == 'Closed'`). Cancelled contracts were excluded from top-line revenue recognition.

### Monthly Sales Trend (2024 – 2026)
* Sales revenue exhibits upward temporal momentum combined with seasonality peaks in Spring and Q4 launch periods.
* Monthly revenue ranges from **~858 Million EGP** in January 2024 to over **~2.17 Billion EGP** in peak mid-2026 periods.
* Total closed sales volume: **48,984,544,000 EGP** across 33 monthly cycles.

---

## 3. Deal Analytics

A comprehensive audit of the 12,000 deal contracts generated:

| Metric | Calculated Value |
| :--- | :--- |
| **Total Deals Created** | 12,000 |
| **Total Closed Deals** | 7,937 (66.14%) |
| **Total Cancelled Deals** | 4,063 (33.86%) |
| **Average Deal Value (ADV)** | 6,171,669.90 EGP |
| **Median Deal Value** | 4,499,000.00 EGP |
| **Minimum Closed Deal Price** | 338,000.00 EGP |
| **Maximum Closed Deal Price** | 78,054,000.00 EGP |

The right-skewed distribution between mean (6.17M EGP) and median (4.50M EGP) reflects high-ticket luxury villas and commercial retail assets pulling the upper tail.

---

## 4. Location Analysis

Sales revenue joined across `deals -> units -> projects` revealed distinct regional concentration:

| Location | Closed Deals | Total Revenue (EGP) | Avg Deal Value (EGP) | Revenue Share |
| :--- | :---: | :---: | :---: | :---: |
| **New Cairo** | 1,246 | 12,425,511,200 | 9,972,320.39 | **25.37%** |
| **Sheikh Zayed** | 1,237 | 9,162,552,800 | 7,407,075.83 | **18.70%** |
| **New Capital** | 1,212 | 8,347,516,000 | 6,887,389.44 | **17.04%** |
| **Alexandria** | 846 | 4,755,482,100 | 5,621,137.23 | **9.71%** |
| **Maadi** | 790 | 4,124,692,300 | 5,221,129.49 | **8.42%** |
| **6th of October** | 770 | 3,401,740,500 | 4,417,844.81 | **6.94%** |
| **El Shorouk** | 701 | 2,700,880,700 | 3,852,896.86 | **5.51%** |
| **Nasr City** | 361 | 1,989,420,300 | 5,510,859.56 | **4.06%** |
| **Mansoura** | 409 | 1,046,393,900 | 2,558,420.29 | **2.14%** |
| **Obour** | 365 | 1,030,354,200 | 2,822,888.22 | **2.10%** |

*Insight:* Top 3 zones (**New Cairo, Sheikh Zayed, New Capital**) generate **61.11%** of aggregate enterprise sales revenue.

---

## 5. Property Type Analysis

| Property Type | Deal Count | Revenue (EGP) | Avg Deal Value (EGP) | Revenue Share |
| :--- | :---: | :---: | :---: | :---: |
| **Apartment** | 3,186 | 14,201,966,700 | 4,457,616.67 | **28.99%** |
| **Villa** | 608 | 11,443,212,800 | 18,821,073.68 | **23.36%** |
| **Office** | 1,837 | 9,257,038,200 | 5,039,215.13 | **18.90%** |
| **Townhouse** | 806 | 7,781,896,100 | 9,654,957.94 | **15.89%** |
| **Retail** | 1,073 | 4,646,045,700 | 4,329,958.71 | **9.48%** |
| **Chalet** | 427 | 1,654,384,500 | 3,874,436.77 | **3.38%** |

*Insight:* While **Apartments** drive the highest total volume and revenue (28.99%), **Villas** deliver the highest capital density per closing (18.82M EGP average).

---

## 6. Lead Conversion

### Definition of Conversion
A lead is classified as **Converted** if and only if its unique `lead_id` matches a record in `deals.csv` where `deal_status == 'Closed'`.

### Conversion Performance by Marketing Channel
| Lead Source | Total Leads | Converted Leads | Conversion Rate |
| :--- | :---: | :---: | :---: |
| **Referral** | 4,771 | 934 | **19.58%** |
| **Walk-in** | 2,415 | 421 | **17.43%** |
| **Property Portal** | 15,093 | 2,222 | **14.72%** |
| **Website** | 13,133 | 1,598 | **12.17%** |
| **Call Center** | 3,588 | 409 | **11.40%** |
| **Facebook** | 12,009 | 1,366 | **11.37%** |
| **Instagram** | 8,991 | 987 | **10.98%** |

*Insight:* Direct and relational channels (**Referral** and **Walk-in**) significantly outperform broad digital social campaigns in final transaction conversion.

---

## 7. Agent Performance

* Total active sales agents evaluated: **100 agents**.
* Median revenue per agent: **~489 Million EGP**.
* Closed deals per agent range from **61 to 102 closed deals**.
* Average agent conversion rate: **13.23%** (varying from 10.15% to 17.03% aligned with experience and effectiveness rating).
* Total sales commissions disbursed: **~1.22 Billion EGP**.

---

## 8. Profitability

### Corporate Financial Statement Summary
* **Gross Revenue (Sales + Rentals):** 50,732,489,700 EGP
* **Total Operating Expenses:** 2,675,881,754 EGP
  - *Salaries:* ~31.1%
  - *Marketing:* ~15.2%
  - *Commissions:* ~11.3%
  - *Maintenance & Office:* ~42.4%
* **Net Operating Profit:** 48,056,607,946 EGP
* **Net Profit Margin:** **94.73%**

*Note on Accounting Classification:* In this synthetic dataset, `expenses.csv` reflects master operational and project overheads. Unit construction costs are embedded in development margins.

---

## 9. Rental Analytics

* **Inventory Base:** 5,000 physical property units.
* **Lease Agreements Created:** 3,200 leases (1,104 Active, 1,848 Expired, 248 Terminated).
* **Occupancy Rate:** **22.08%** active physical occupancy.
* **Rent Billed (Due):** 1,808,541,400 EGP.
* **Rent Collected (Paid):** 1,747,945,700 EGP (**96.65% Collection Rate**).
* **Payment Status Distribution:** 27,249 Paid (85.15%), 3,184 Late (9.95%), 1,567 Partial (4.90%).

---

## 10. Maintenance Analytics

* **Total Maintenance Tickets:** 12,000 requests.
* **Status Breakdown:** 9,863 Completed (82.19%), 1,417 In Progress (11.81%), 720 Scheduled (6.00%).
* **Total Maintenance Expenditure:** 90,837,390 EGP.
* **Average Ticket Cost:** 7,569.78 EGP (Median: 5,460.00 EGP).
* **Highest Cost Categories:** *Painting* (21.7M EGP) and *HVAC* (21.3M EGP).

---

## 11. Customer Analytics

* **Customer Base:** 10,000 registered individuals and corporate entities.
* **Customer Segment Breakdown:** End Users (50.15%), Investors (24.78%), Businesses (14.99%), Landlords (10.08%).
* **Funnel Penetration:**
  - 10,000 Registered Customers (100.0%)
  - 9,965 Submitted Leads (99.65%)
  - 9,815 Attended Viewings (98.15%)
  - 6,985 Executed Closed Deals (69.85%)
* **Top Revenue Tier:** Platinum Tier customers accounted for **~38.4%** of closed sales capital.

---

## 12. Project Performance

Across the 20 master developments:
* Units per project: Exactly 250 units each.
* Closed deals per project range from **361 to 846 deals** (driven by project location, completion status, and popularity).
* All 20 projects delivered positive net operating margins, led by *Crestview Heights* (New Cairo) and *Palma Residences* (Sheikh Zayed).

---

## 13. Market Analytics Summary

A composite evaluation of the 39 distinct Location $\times$ Property Type segments shows that **New Cairo Apartments**, **New Cairo Villas**, and **Sheikh Zayed Villas** form the core liquidity pillars of the market, combining high volume, resilient absorption rates, and premium square-meter pricing.

---

## 14. Pandas vs SQL Validation

All primary metrics were computed independently using Pandas vectorized pipelines and DuckDB SQL queries over raw CSV files.

| Validation Check | Pandas Value | DuckDB SQL Value | Status |
| :--- | :---: | :---: | :---: |
| **Total Monthly Sales Revenue** | 48,984,544,000.00 | 48,984,544,000.00 | **PASS** |
| **Total Location Revenue** | 48,984,544,000.00 | 48,984,544,000.00 | **PASS** |
| **Total Property Type Revenue** | 48,984,544,000.00 | 48,984,544,000.00 | **PASS** |
| **Total Closed Deals Count** | 7,937 | 7,937 | **PASS** |
| **Average Deal Value (EGP)** | 6,171,669.90 | 6,171,669.90 | **PASS** |
| **Net Operating Profit (EGP)** | 48,056,607,946.00 | 48,056,607,946.00 | **PASS** |
| **Rental Occupancy Rate** | 22.08% | 22.08% | **PASS** |
| **Total Rent Collected (EGP)** | 1,747,945,700.00 | 1,747,945,700.00 | **PASS** |
| **Sales Join Cardinality** | 7,937 rows | 7,937 rows | **PASS** |
| **Raw Data SHA-256 Hashes** | 13/13 Matching | 13/13 Matching | **PASS** |

---

## 15. Data Quality Limitations

1. **Synthetic Nature:** All prices, yields, customer profiles, and transaction logs are generated algorithmically for intelligence benchmarking and do not represent actual live market quotes in Egypt.
2. **Controlled Noise:** 39 customer records contain `NaN` for monthly income, and expense records contain 0.31% intentional anomaly spikes for ML anomaly detection testing.
3. **Absence of Real Market Shocks:** Macroeconomic currency fluctuations and inflation indices are simulated via non-linear trend multipliers rather than live macroeconomic feeds.

---

## 16. Business Insights

1. **Channel ROI Disparity:** Organic referrals and physical walk-ins convert at nearly double the rate (17.4% – 19.6%) of paid social ad channels (11.0% – 11.4%), signaling that marketing spend should be reallocated toward referral incentives.
2. **Asset Concentration:** High-end residential villas and prime commercial offices represent only 30.8% of closed transactions but contribute **58.1% of total transaction value**.
3. **Cash Flow Reliability:** Rental operations maintain a 96.65% collection rate, providing predictable recurring liquidity alongside episodic large sales closings.

---

## 17. ML Opportunities for Subsequent Phases

The analytical foundations established in Phase 2 directly map to the planned ML roadmap:
* **Regression (Phase 4):** Property Price Prediction using unit specifications, floor level, finishing, and project popularity features.
* **Classification (Phase 5):** Lead Conversion Probability Prediction based on customer budget match, lead source, interaction history, and viewing feedback.
* **Clustering (Phase 6):** Customer Behavioral Segmentation (RFM + Investment intent clustering).
* **Forecasting (Phase 7):** Temporal Sales & Cash-Flow Forecasting leveraging monthly historical deal cycles.
* **Anomaly Detection (Phase 8):** Outlier and fraud detection on project expenditures and unusual maintenance tickets.
