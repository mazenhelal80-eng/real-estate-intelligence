export interface PropertyRecord {
  unit_id: string;
  project_id: string;
  project_name: string;
  developer_name: string;
  location: string;
  property_type: string;
  area_sqm: number;
  bedrooms: number;
  bathrooms: number;
  floor_number: number;
  finishing_type: string;
  base_price_egp: number;
  expected_rent_monthly_egp: number;
  construction_status: string;
  popularity_score: number;
}

export interface DeveloperStat {
  developer_name: string;
  total_units: number;
  active_projects: number;
  avg_price_egp: number;
  location: string;
}

export interface MonthlyRevenuePoint {
  month: string;
  deal_revenue_egp: number;
  rental_revenue_egp: number;
  total_revenue_egp: number;
  expenses_egp: number;
  net_profit_egp: number;
}

export interface LocationRevenuePoint {
  location: string;
  revenue_egp: number;
  deals_count: number;
  avg_deal_price_egp: number;
}

export interface PropertyTypeStat {
  property_type: string;
  units_count: number;
  avg_price_per_sqm: number;
  avg_price_egp: number;
}
