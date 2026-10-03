"""
Phase 2 - Section 2.13: SQL Analytics Layer using DuckDB
Purpose: Query raw CSVs via SQL to compute analytical datasets and validate against Pandas.
Outputs: reports/sql/*.csv
"""

from pathlib import Path
import duckdb
import pandas as pd


def run_sql_analytics():
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "real_estate_intelligence_dataset" / "raw"
    sql_reports_dir = project_root / "reports" / "sql"
    sql_reports_dir.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(database=":memory:")

    # Register raw CSV tables as SQL views
    tables = [
        "projects", "units", "customers", "agents", "listings",
        "leads", "viewings", "deals", "expenses", "tenants",
        "leases", "rent_payments", "maintenance"
    ]

    for tbl in tables:
        csv_path = (raw_dir / f"{tbl}.csv").as_posix()
        con.execute(f"CREATE VIEW {tbl} AS SELECT * FROM read_csv_auto('{csv_path}')")

    print(f"Registered {len(tables)} raw tables in DuckDB SQL memory engine.")

    # 1. Monthly Revenue SQL
    monthly_rev_sql = """
    SELECT 
        strftime(CAST(deal_date AS DATE), '%Y-%m') AS year_month,
        SUM(deal_price_egp) AS revenue_egp,
        COUNT(deal_id) AS closed_deals_count,
        ROUND(AVG(deal_price_egp), 2) AS average_deal_value_egp,
        ROUND(MEDIAN(deal_price_egp), 2) AS median_deal_value_egp,
        MIN(deal_price_egp) AS min_deal_value_egp,
        MAX(deal_price_egp) AS max_deal_value_egp
    FROM deals
    WHERE deal_status = 'Closed'
    GROUP BY strftime(CAST(deal_date AS DATE), '%Y-%m')
    ORDER BY year_month ASC
    """
    df_monthly_rev = con.execute(monthly_rev_sql).df()
    df_monthly_rev.to_csv(sql_reports_dir / "monthly_revenue_sql.csv", index=False, encoding="utf-8")

    # 2. Revenue by Location SQL
    rev_by_loc_sql = """
    WITH closed_deals AS (
        SELECT d.deal_id, d.deal_price_egp, p.location
        FROM deals d
        JOIN units u ON d.unit_id = u.unit_id
        JOIN projects p ON u.project_id = p.project_id
        WHERE d.deal_status = 'Closed'
    ),
    loc_totals AS (
        SELECT 
            location,
            SUM(deal_price_egp) AS revenue_egp,
            COUNT(deal_id) AS closed_deals_count,
            ROUND(AVG(deal_price_egp), 2) AS average_deal_value_egp
        FROM closed_deals
        GROUP BY location
    ),
    grand_total AS (
        SELECT SUM(revenue_egp) AS total_revenue FROM loc_totals
    )
    SELECT 
        l.location,
        l.revenue_egp,
        l.closed_deals_count,
        l.average_deal_value_egp,
        ROUND((l.revenue_egp * 100.0) / g.total_revenue, 2) AS revenue_percentage
    FROM loc_totals l, grand_total g
    ORDER BY l.revenue_egp DESC
    """
    df_rev_loc = con.execute(rev_by_loc_sql).df()
    df_rev_loc.to_csv(sql_reports_dir / "revenue_by_location_sql.csv", index=False, encoding="utf-8")

    # 3. Revenue by Property Type SQL
    rev_by_prop_sql = """
    WITH closed_deals AS (
        SELECT d.deal_id, d.deal_price_egp, u.property_type
        FROM deals d
        JOIN units u ON d.unit_id = u.unit_id
        WHERE d.deal_status = 'Closed'
    ),
    prop_totals AS (
        SELECT 
            property_type,
            SUM(deal_price_egp) AS revenue_egp,
            COUNT(deal_id) AS deal_count,
            ROUND(AVG(deal_price_egp), 2) AS average_deal_value_egp
        FROM closed_deals
        GROUP BY property_type
    ),
    grand_total AS (
        SELECT SUM(revenue_egp) AS total_revenue FROM prop_totals
    )
    SELECT 
        p.property_type,
        p.revenue_egp,
        p.deal_count,
        p.average_deal_value_egp,
        ROUND((p.revenue_egp * 100.0) / g.total_revenue, 2) AS revenue_percentage
    FROM prop_totals p, grand_total g
    ORDER BY p.revenue_egp DESC
    """
    df_rev_prop = con.execute(rev_by_prop_sql).df()
    df_rev_prop.to_csv(sql_reports_dir / "revenue_by_property_type_sql.csv", index=False, encoding="utf-8")

    # 4. Deal Metrics SQL
    deal_metrics_sql = """
    SELECT 
        COUNT(*) AS total_deals_created,
        SUM(CASE WHEN deal_status = 'Closed' THEN 1 ELSE 0 END) AS total_closed_deals,
        SUM(CASE WHEN deal_status = 'Cancelled' THEN 1 ELSE 0 END) AS total_cancelled_deals,
        ROUND(SUM(CASE WHEN deal_status = 'Cancelled' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS cancellation_rate_percentage,
        SUM(CASE WHEN deal_status = 'Closed' THEN deal_price_egp ELSE 0 END) AS total_closed_revenue_egp,
        ROUND(AVG(CASE WHEN deal_status = 'Closed' THEN deal_price_egp ELSE NULL END), 2) AS average_deal_value_egp,
        ROUND(MEDIAN(CASE WHEN deal_status = 'Closed' THEN deal_price_egp ELSE NULL END), 2) AS median_deal_value_egp,
        MIN(CASE WHEN deal_status = 'Closed' THEN deal_price_egp ELSE NULL END) AS min_deal_value_egp,
        MAX(CASE WHEN deal_status = 'Closed' THEN deal_price_egp ELSE NULL END) AS max_deal_value_egp
    FROM deals
    """
    df_deal_metrics = con.execute(deal_metrics_sql).df()
    df_deal_metrics.to_csv(sql_reports_dir / "deal_metrics_sql.csv", index=False, encoding="utf-8")

    monthly_deal_metrics_sql = """
    SELECT 
        strftime(CAST(deal_date AS DATE), '%Y-%m') AS year_month,
        COUNT(*) AS total_deals,
        SUM(CASE WHEN deal_status = 'Closed' THEN 1 ELSE 0 END) AS closed_deals,
        SUM(CASE WHEN deal_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_deals,
        SUM(CASE WHEN deal_status = 'Closed' THEN deal_price_egp ELSE 0 END) AS revenue_egp,
        ROUND(AVG(CASE WHEN deal_status = 'Closed' THEN deal_price_egp ELSE NULL END), 2) AS average_deal_value_egp,
        ROUND(MEDIAN(CASE WHEN deal_status = 'Closed' THEN deal_price_egp ELSE NULL END), 2) AS median_deal_value_egp,
        ROUND(SUM(CASE WHEN deal_status = 'Cancelled' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS cancellation_rate_percentage
    FROM deals
    GROUP BY strftime(CAST(deal_date AS DATE), '%Y-%m')
    ORDER BY year_month ASC
    """
    df_monthly_deals = con.execute(monthly_deal_metrics_sql).df()
    df_monthly_deals.to_csv(sql_reports_dir / "monthly_deal_metrics_sql.csv", index=False, encoding="utf-8")

    # 5. Lead Conversion by Source SQL
    lead_conv_sql = """
    WITH closed_leads AS (
        SELECT DISTINCT lead_id FROM deals WHERE deal_status = 'Closed'
    )
    SELECT 
        l.lead_source,
        COUNT(l.lead_id) AS total_leads,
        SUM(CASE WHEN cl.lead_id IS NOT NULL THEN 1 ELSE 0 END) AS converted_leads,
        SUM(CASE WHEN l.lead_status = 'Qualified' THEN 1 ELSE 0 END) AS qualified_leads,
        ROUND(SUM(CASE WHEN cl.lead_id IS NOT NULL THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(l.lead_id), 2) AS conversion_rate_percentage
    FROM leads l
    LEFT JOIN closed_leads cl ON l.lead_id = cl.lead_id
    GROUP BY l.lead_source
    ORDER BY converted_leads DESC
    """
    df_lead_conv = con.execute(lead_conv_sql).df()
    df_lead_conv.to_csv(sql_reports_dir / "lead_conversion_by_source_sql.csv", index=False, encoding="utf-8")

    # 6. Agent Performance SQL
    agent_perf_sql = """
    WITH a_leads AS (
        SELECT agent_id, COUNT(lead_id) AS leads_count FROM leads GROUP BY agent_id
    ),
    a_viewings AS (
        SELECT agent_id, COUNT(viewing_id) AS viewings_count FROM viewings GROUP BY agent_id
    ),
    a_deals AS (
        SELECT 
            agent_id,
            COUNT(deal_id) AS total_deals_count,
            SUM(CASE WHEN deal_status = 'Closed' THEN 1 ELSE 0 END) AS closed_deals_count,
            SUM(CASE WHEN deal_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_deals_count,
            SUM(CASE WHEN deal_status = 'Closed' THEN deal_price_egp ELSE 0 END) AS revenue_egp,
            SUM(CASE WHEN deal_status = 'Closed' THEN commission_amount_egp ELSE 0 END) AS commission_earned_egp
        FROM deals
        GROUP BY agent_id
    )
    SELECT 
        a.agent_id,
        a.agent_name,
        a.email,
        a.phone_number,
        a.team_name,
        a.specialization,
        a.assigned_location,
        a.experience_years,
        a.effectiveness_rating,
        a.hire_date,
        COALESCE(al.leads_count, 0) AS leads_count,
        COALESCE(av.viewings_count, 0) AS viewings_count,
        COALESCE(ad.total_deals_count, 0) AS total_deals_count,
        COALESCE(ad.closed_deals_count, 0) AS closed_deals_count,
        COALESCE(ad.cancelled_deals_count, 0) AS cancelled_deals_count,
        COALESCE(ad.revenue_egp, 0) AS revenue_egp,
        COALESCE(ad.commission_earned_egp, 0) AS commission_earned_egp,
        ROUND(COALESCE(ad.revenue_egp, 0) * 1.0 / NULLIF(COALESCE(ad.closed_deals_count, 0), 0), 2) AS average_deal_value_egp,
        ROUND(COALESCE(ad.closed_deals_count, 0) * 100.0 / NULLIF(COALESCE(al.leads_count, 0), 0), 2) AS conversion_rate_percentage
    FROM agents a
    LEFT JOIN a_leads al ON a.agent_id = al.agent_id
    LEFT JOIN a_viewings av ON a.agent_id = av.agent_id
    LEFT JOIN a_deals ad ON a.agent_id = ad.agent_id
    ORDER BY revenue_egp DESC
    """
    df_agent_perf = con.execute(agent_perf_sql).df()
    df_agent_perf.to_csv(sql_reports_dir / "agent_performance_sql.csv", index=False, encoding="utf-8")

    # 7. Profitability Summary SQL
    profit_summary_sql = """
    WITH rev AS (
        SELECT 
            (SELECT SUM(deal_price_egp) FROM deals WHERE deal_status = 'Closed') AS sales_rev,
            (SELECT SUM(amount_paid_egp) FROM rent_payments) AS rental_rev,
            (SELECT SUM(amount_egp) FROM expenses) AS total_exp
    )
    SELECT 
        sales_rev AS total_sales_revenue_egp,
        rental_rev AS total_rental_revenue_egp,
        sales_rev + rental_rev AS gross_revenue_egp,
        total_exp AS total_operating_expenses_egp,
        (sales_rev + rental_rev) - total_exp AS net_operating_profit_egp,
        ROUND(((sales_rev + rental_rev - total_exp) * 100.0) / (sales_rev + rental_rev), 2) AS net_profit_margin_percentage
    FROM rev
    """
    df_profit_summary = con.execute(profit_summary_sql).df()
    df_profit_summary.to_csv(sql_reports_dir / "profitability_summary_sql.csv", index=False, encoding="utf-8")

    # 8. Rental Metrics SQL
    rental_metrics_sql = """
    SELECT 
        (SELECT COUNT(*) FROM units) AS total_rentable_units_inventory,
        (SELECT COUNT(*) FROM leases) AS total_leases_created,
        (SELECT COUNT(*) FROM leases WHERE lease_status = 'Active') AS active_leases_count,
        (SELECT COUNT(*) FROM leases WHERE lease_status = 'Expired') AS expired_leases_count,
        (SELECT COUNT(*) FROM leases WHERE lease_status = 'Terminated') AS terminated_leases_count,
        (SELECT COUNT(DISTINCT unit_id) FROM leases WHERE lease_status = 'Active') AS active_occupied_units_count,
        ROUND((SELECT COUNT(DISTINCT unit_id) FROM leases WHERE lease_status = 'Active') * 100.0 / (SELECT COUNT(*) FROM units), 2) AS occupancy_rate_percentage,
        (SELECT SUM(amount_due_egp) FROM rent_payments) AS total_rent_due_egp,
        (SELECT SUM(amount_paid_egp) FROM rent_payments) AS total_rent_collected_egp,
        ROUND((SELECT SUM(amount_paid_egp) FROM rent_payments) * 100.0 / (SELECT SUM(amount_due_egp) FROM rent_payments), 2) AS collection_rate_percentage
    """
    df_rental_metrics = con.execute(rental_metrics_sql).df()
    df_rental_metrics.to_csv(sql_reports_dir / "rental_metrics_sql.csv", index=False, encoding="utf-8")

    # 9. Maintenance Metrics SQL
    maintenance_metrics_sql = """
    SELECT 
        COUNT(*) * 1.0 AS total_maintenance_tickets,
        SUM(CASE WHEN status = 'Completed' THEN 1.0 ELSE 0.0 END) AS completed_tickets_count,
        SUM(CASE WHEN status = 'In Progress' THEN 1.0 ELSE 0.0 END) AS in_progress_tickets_count,
        SUM(CASE WHEN status = 'Scheduled' THEN 1.0 ELSE 0.0 END) AS scheduled_tickets_count,
        SUM(cost_egp) * 1.0 AS total_maintenance_expenditure_egp,
        ROUND(AVG(cost_egp), 2) AS average_ticket_cost_egp,
        ROUND(MEDIAN(cost_egp), 2) AS median_ticket_cost_egp,
        ROUND(SUM(CASE WHEN status = 'Completed' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS completion_rate_percentage
    FROM maintenance
    """
    df_maint_metrics = con.execute(maintenance_metrics_sql).df()
    df_maint_metrics_unpivoted = pd.DataFrame({
        "metric": [
            "total_maintenance_tickets", "completed_tickets_count", "in_progress_tickets_count",
            "scheduled_tickets_count", "total_maintenance_expenditure_egp", "average_ticket_cost_egp",
            "median_ticket_cost_egp", "completion_rate_percentage"
        ],
        "value": [
            df_maint_metrics["total_maintenance_tickets"].iloc[0],
            df_maint_metrics["completed_tickets_count"].iloc[0],
            df_maint_metrics["in_progress_tickets_count"].iloc[0],
            df_maint_metrics["scheduled_tickets_count"].iloc[0],
            df_maint_metrics["total_maintenance_expenditure_egp"].iloc[0],
            df_maint_metrics["average_ticket_cost_egp"].iloc[0],
            df_maint_metrics["median_ticket_cost_egp"].iloc[0],
            df_maint_metrics["completion_rate_percentage"].iloc[0]
        ]
    })
    df_maint_metrics_unpivoted.to_csv(sql_reports_dir / "maintenance_metrics_sql.csv", index=False, encoding="utf-8")

    # 10. Project Performance SQL
    project_perf_sql = """
    WITH prj_units AS (
        SELECT project_id, COUNT(unit_id) AS total_units_count
        FROM units
        GROUP BY project_id
    ),
    prj_listings AS (
        SELECT u.project_id, COUNT(DISTINCT l.unit_id) AS listed_units_count
        FROM listings l
        JOIN units u ON l.unit_id = u.unit_id
        GROUP BY u.project_id
    ),
    prj_deals AS (
        SELECT 
            u.project_id,
            COUNT(d.deal_id) AS closed_deals_count,
            SUM(d.deal_price_egp) AS revenue_egp
        FROM deals d
        JOIN units u ON d.unit_id = u.unit_id
        WHERE d.deal_status = 'Closed'
        GROUP BY u.project_id
    ),
    prj_expenses AS (
        SELECT project_id, SUM(amount_egp) AS total_expenses_egp
        FROM expenses
        GROUP BY project_id
    )
    SELECT 
        p.project_id,
        p.project_name,
        p.developer_name,
        p.project_type,
        p.location,
        p.launch_date,
        p.expected_completion_date,
        p.target_total_units,
        p.popularity_score,
        p.construction_status,
        COALESCE(pu.total_units_count, 0) AS total_units_count,
        COALESCE(pl.listed_units_count, 0) AS listed_units_count,
        COALESCE(pd.closed_deals_count, 0) AS closed_deals_count,
        COALESCE(pd.revenue_egp, 0) AS revenue_egp,
        COALESCE(pe.total_expenses_egp, 0) AS total_expenses_egp,
        ROUND(COALESCE(pd.revenue_egp, 0) * 1.0 / NULLIF(COALESCE(pd.closed_deals_count, 0), 0), 2) AS average_deal_value_egp,
        COALESCE(pd.revenue_egp, 0) - COALESCE(pe.total_expenses_egp, 0) AS net_project_profit_egp,
        ROUND((COALESCE(pd.revenue_egp, 0) - COALESCE(pe.total_expenses_egp, 0)) * 100.0 / NULLIF(COALESCE(pd.revenue_egp, 0), 0), 2) AS profit_margin_percentage
    FROM projects p
    LEFT JOIN prj_units pu ON p.project_id = pu.project_id
    LEFT JOIN prj_listings pl ON p.project_id = pl.project_id
    LEFT JOIN prj_deals pd ON p.project_id = pd.project_id
    LEFT JOIN prj_expenses pe ON p.project_id = pe.project_id
    ORDER BY revenue_egp DESC
    """
    df_project_perf = con.execute(project_perf_sql).df()
    df_project_perf.to_csv(sql_reports_dir / "project_performance_sql.csv", index=False, encoding="utf-8")

    print(f"-> Generated all SQL analytics datasets in {sql_reports_dir.relative_to(project_root)}")
    return True


if __name__ == "__main__":
    run_sql_analytics()

