"""
Phase 2 - Section 2.5: Lead Conversion Analytics
Purpose: Compute end-to-end lead conversion rates overall and segmented across dimensions.
Outputs:
  - reports/lead_conversion_metrics.csv
  - reports/lead_conversion_by_source.csv
  - reports/lead_conversion_by_customer_type.csv
  - reports/lead_conversion_by_location.csv
  - reports/lead_conversion_by_property_type.csv
"""

from pathlib import Path
import pandas as pd


def compute_lead_conversion():
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "real_estate_intelligence_dataset" / "raw"
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    leads_df = pd.read_csv(raw_dir / "leads.csv")
    deals_df = pd.read_csv(raw_dir / "deals.csv")
    customers_df = pd.read_csv(raw_dir / "customers.csv")
    units_df = pd.read_csv(raw_dir / "units.csv")
    projects_df = pd.read_csv(raw_dir / "projects.csv")

    # Set of lead_ids that resulted in closed deals
    closed_deals = deals_df[deals_df["deal_status"] == "Closed"]
    closed_lead_ids = set(closed_deals["lead_id"].dropna().unique())

    # Add conversion flag to leads
    leads_df["is_converted"] = leads_df["lead_id"].isin(closed_lead_ids)

    total_leads = len(leads_df)
    qualified_leads = int((leads_df["lead_status"] == "Qualified").sum())
    converted_leads = int(leads_df["is_converted"].sum())
    overall_conv_rate = round((converted_leads / total_leads) * 100, 2)
    qualified_conv_rate = round((converted_leads / qualified_leads) * 100, 2) if qualified_leads > 0 else 0.0

    overall_metrics = pd.DataFrame([
        {"metric": "total_leads", "value": total_leads},
        {"metric": "qualified_leads", "value": qualified_leads},
        {"metric": "converted_leads_closed_deals", "value": converted_leads},
        {"metric": "overall_conversion_rate_percentage", "value": overall_conv_rate},
        {"metric": "qualified_conversion_rate_percentage", "value": qualified_conv_rate},
        {"metric": "conversion_definition", "value": "A lead is converted if its lead_id exists in deals.csv with deal_status == 'Closed'"}
    ])

    # 1. By Source
    by_source = (
        leads_df.groupby("lead_source", as_index=False)
        .agg(
            total_leads=("lead_id", "count"),
            converted_leads=("is_converted", "sum"),
            qualified_leads=("lead_status", lambda s: (s == "Qualified").sum())
        )
        .sort_values("converted_leads", ascending=False)
        .reset_index(drop=True)
    )
    by_source["conversion_rate_percentage"] = (
        (by_source["converted_leads"] / by_source["total_leads"]) * 100
    ).round(2)

    # 2. By Customer Type
    leads_with_cust = leads_df.merge(customers_df[["customer_id", "customer_type"]], on="customer_id", how="inner")
    by_cust_type = (
        leads_with_cust.groupby("customer_type", as_index=False)
        .agg(
            total_leads=("lead_id", "count"),
            converted_leads=("is_converted", "sum"),
        )
        .sort_values("converted_leads", ascending=False)
        .reset_index(drop=True)
    )
    by_cust_type["conversion_rate_percentage"] = (
        (by_cust_type["converted_leads"] / by_cust_type["total_leads"]) * 100
    ).round(2)

    # 3. By Location (leads -> units -> projects)
    leads_with_units = leads_df.merge(units_df[["unit_id", "project_id", "property_type"]], on="unit_id", how="inner")
    leads_with_proj = leads_with_units.merge(projects_df[["project_id", "location"]], on="project_id", how="inner")

    by_location = (
        leads_with_proj.groupby("location", as_index=False)
        .agg(
            total_leads=("lead_id", "count"),
            converted_leads=("is_converted", "sum"),
        )
        .sort_values("converted_leads", ascending=False)
        .reset_index(drop=True)
    )
    by_location["conversion_rate_percentage"] = (
        (by_location["converted_leads"] / by_location["total_leads"]) * 100
    ).round(2)

    # 4. By Property Type
    by_property_type = (
        leads_with_proj.groupby("property_type", as_index=False)
        .agg(
            total_leads=("lead_id", "count"),
            converted_leads=("is_converted", "sum"),
        )
        .sort_values("converted_leads", ascending=False)
        .reset_index(drop=True)
    )
    by_property_type["conversion_rate_percentage"] = (
        (by_property_type["converted_leads"] / by_property_type["total_leads"]) * 100
    ).round(2)

    # Save reports
    overall_metrics.to_csv(reports_dir / "lead_conversion_metrics.csv", index=False, encoding="utf-8")
    by_source.to_csv(reports_dir / "lead_conversion_by_source.csv", index=False, encoding="utf-8")
    by_cust_type.to_csv(reports_dir / "lead_conversion_by_customer_type.csv", index=False, encoding="utf-8")
    by_location.to_csv(reports_dir / "lead_conversion_by_location.csv", index=False, encoding="utf-8")
    by_property_type.to_csv(reports_dir / "lead_conversion_by_property_type.csv", index=False, encoding="utf-8")

    print(f"-> Generated lead conversion reports in {reports_dir.relative_to(project_root)}")
    return overall_metrics, by_source, by_cust_type, by_location, by_property_type


if __name__ == "__main__":
    compute_lead_conversion()
