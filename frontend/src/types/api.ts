export interface HealthResponse {
  status: string;
  version: string;
}

export interface PricePredictionRequest {
  area_sqm: number;
  bedrooms: number;
  bathrooms: number;
  floor_number: number;
  property_age: number;
  room_density: number;
  popularity_score: number;
  property_type_Apartment: number;
  property_type_Chalet: number;
  property_type_Office: number;
  property_type_Retail: number;
  property_type_Townhouse: number;
  property_type_Villa: number;
  "finishing_type_Core & Shell": number;
  "finishing_type_Fully Finished": number;
  "finishing_type_Semi Finished": number;
  "finishing_type_Ultra Super Lux": number;
  "location_6th of October": number;
  location_Alexandria: number;
  "location_El Shorouk": number;
  location_Maadi: number;
  location_Mansoura: number;
  "location_Nasr City": number;
  "location_New Cairo": number;
  "location_New Capital": number;
  location_Obour: number;
  "location_Sheikh Zayed": number;
  "developer_name_Emaar Misr Prime": number;
  "developer_name_Hassan Allam Properties": number;
  "developer_name_Misr Italia Urban": number;
  "developer_name_Mountain View East": number;
  "developer_name_Orascom Development": number;
  "developer_name_Palm Hills Legacy": number;
  "developer_name_Sodic Prestige": number;
  "developer_name_Talaat Moustafa Group": number;
  construction_status_Planning: number;
  "construction_status_Under Construction": number;
}

export interface PricePredictionResponse {
  model_name: string;
  model_version: string;
  predicted_price_egp: number;
  target_name: string;
}

export interface LeadConversionRequest {
  lead_score: number;
  interaction_count: number;
  monthly_income_egp: number;
  budget_max_egp: number;
  budget_spread_egp: number;
  income_to_budget_ratio: number;
  listing_price_egp: number;
  "lead_source_Call Center": number;
  lead_source_Facebook: number;
  lead_source_Instagram: number;
  "lead_source_Property Portal": number;
  lead_source_Referral: number;
  "lead_source_Walk-in": number;
  lead_source_Website: number;
  customer_type_Business: number;
  "customer_type_End User": number;
  customer_type_Investor: number;
  customer_type_Landlord: number;
  customer_tier_Bronze: number;
  customer_tier_Gold: number;
  customer_tier_Platinum: number;
  customer_tier_Silver: number;
  interaction_frequency_High: number;
  interaction_frequency_Low: number;
  interaction_frequency_Medium: number;
  listing_type_Rent: number;
  listing_type_Sale: number;
}

export interface LeadConversionResponse {
  model_name: string;
  model_version: string;
  probability: number;
  threshold: number;
  prediction: number;
  class_label: string;
}

export interface CustomerSegmentationRequest {
  budget_min_egp: number;
  budget_max_egp: number;
  budget_spread_egp: number;
  monthly_income_egp: number;
  income_to_budget_ratio: number;
  customer_type_Business: number;
  "customer_type_End User": number;
  customer_type_Investor: number;
  customer_type_Landlord: number;
  customer_tier_Bronze: number;
  customer_tier_Gold: number;
  customer_tier_Platinum: number;
  customer_tier_Silver: number;
  interaction_frequency_High: number;
  interaction_frequency_Low: number;
  interaction_frequency_Medium: number;
}

export interface CustomerSegmentationResponse {
  model_name: string;
  model_version: string;
  cluster_id: number;
}

export interface PropertyAnomalyRequest {
  area_sqm: number;
  bedrooms: number;
  bathrooms: number;
  floor_number: number;
  base_price_egp: number;
  expected_rent_monthly_egp: number;
  price_per_sqm: number;
  property_age: number;
  rental_yield: number;
  room_density: number;
  popularity_score: number;
}

export interface PropertyAnomalyResponse {
  model_name: string;
  model_version: string;
  anomaly_flag: number;
  anomaly_score: number;
}

export interface DailyCashFlowRecord {
  date: string;
  net_cash_flow: number;
}

export interface CashFlowForecastRequest {
  forecast_date?: string;
  historical_series?: DailyCashFlowRecord[];
  lag_1?: number;
  lag_7?: number;
  lag_14?: number;
  lag_28?: number;
  lag_30?: number;
  rolling_mean_7?: number;
  rolling_mean_14?: number;
  rolling_mean_28?: number;
  rolling_std_7?: number;
  rolling_std_28?: number;
  rolling_min_7?: number;
  rolling_max_7?: number;
  day_of_week?: number;
  day_of_month?: number;
  month?: number;
  quarter?: number;
  is_weekend?: number;
}

export interface CashFlowForecastResponse {
  model_name: string;
  model_version: string;
  forecast_date: string;
  predicted_net_cash_flow: number;
}

export interface SegmentCustomerRecord {
  customer_id: string;
  customer_type: string;
  customer_tier: string;
  budget_min_egp: number;
  budget_max_egp: number;
  monthly_income_egp: number;
  interaction_frequency: string;
  preferred_location: string;
  preferred_property_type: string;
}
