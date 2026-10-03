from typing import Optional, List
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"

class PricePredictionRequest(BaseModel):
    area_sqm: float
    bedrooms: float
    bathrooms: float
    floor_number: float
    property_age: float
    room_density: float
    popularity_score: float
    property_type_Apartment: float
    property_type_Chalet: float
    property_type_Office: float
    property_type_Retail: float
    property_type_Townhouse: float
    property_type_Villa: float
    finishing_type_Core_and_Shell: float = Field(alias="finishing_type_Core & Shell")
    finishing_type_Fully_Finished: float = Field(alias="finishing_type_Fully Finished")
    finishing_type_Semi_Finished: float = Field(alias="finishing_type_Semi Finished")
    finishing_type_Ultra_Super_Lux: float = Field(alias="finishing_type_Ultra Super Lux")
    location_6th_of_October: float = Field(alias="location_6th of October")
    location_Alexandria: float
    location_El_Shorouk: float = Field(alias="location_El Shorouk")
    location_Maadi: float
    location_Mansoura: float
    location_Nasr_City: float = Field(alias="location_Nasr City")
    location_New_Cairo: float = Field(alias="location_New Cairo")
    location_New_Capital: float = Field(alias="location_New Capital")
    location_Obour: float
    location_Sheikh_Zayed: float = Field(alias="location_Sheikh Zayed")
    developer_name_Emaar_Misr_Prime: float = Field(alias="developer_name_Emaar Misr Prime")
    developer_name_Hassan_Allam_Properties: float = Field(alias="developer_name_Hassan Allam Properties")
    developer_name_Misr_Italia_Urban: float = Field(alias="developer_name_Misr Italia Urban")
    developer_name_Mountain_View_East: float = Field(alias="developer_name_Mountain View East")
    developer_name_Orascom_Development: float = Field(alias="developer_name_Orascom Development")
    developer_name_Palm_Hills_Legacy: float = Field(alias="developer_name_Palm Hills Legacy")
    developer_name_Sodic_Prestige: float = Field(alias="developer_name_Sodic Prestige")
    developer_name_Talaat_Moustafa_Group: float = Field(alias="developer_name_Talaat Moustafa Group")
    construction_status_Planning: float
    construction_status_Under_Construction: float = Field(alias="construction_status_Under Construction")

    class Config:
        populate_by_name = True

class PricePredictionResponse(BaseModel):
    model_name: str
    model_version: str
    predicted_price_egp: float
    target_name: str

class LeadConversionRequest(BaseModel):
    lead_score: float
    interaction_count: float
    monthly_income_egp: float
    budget_max_egp: float
    budget_spread_egp: float
    income_to_budget_ratio: float
    listing_price_egp: float
    lead_source_Call_Center: float = Field(alias="lead_source_Call Center")
    lead_source_Facebook: float
    lead_source_Instagram: float
    lead_source_Property_Portal: float = Field(alias="lead_source_Property Portal")
    lead_source_Referral: float
    lead_source_Walk_in: float = Field(alias="lead_source_Walk-in")
    lead_source_Website: float
    customer_type_Business: float
    customer_type_End_User: float = Field(alias="customer_type_End User")
    customer_type_Investor: float
    customer_type_Landlord: float
    customer_tier_Bronze: float
    customer_tier_Gold: float
    customer_tier_Platinum: float
    customer_tier_Silver: float
    interaction_frequency_High: float
    interaction_frequency_Low: float
    interaction_frequency_Medium: float
    listing_type_Rent: float
    listing_type_Sale: float

    class Config:
        populate_by_name = True

class LeadConversionResponse(BaseModel):
    model_name: str
    model_version: str
    probability: float
    threshold: float
    prediction: int
    class_label: str

class CustomerSegmentationRequest(BaseModel):
    budget_min_egp: float
    budget_max_egp: float
    budget_spread_egp: float
    monthly_income_egp: float
    income_to_budget_ratio: float
    customer_type_Business: float
    customer_type_End_User: float = Field(alias="customer_type_End User")
    customer_type_Investor: float
    customer_type_Landlord: float
    customer_tier_Bronze: float
    customer_tier_Gold: float
    customer_tier_Platinum: float
    customer_tier_Silver: float
    interaction_frequency_High: float
    interaction_frequency_Low: float
    interaction_frequency_Medium: float

    class Config:
        populate_by_name = True

class CustomerSegmentationResponse(BaseModel):
    model_name: str
    model_version: str
    cluster_id: int

class PropertyAnomalyRequest(BaseModel):
    area_sqm: float
    bedrooms: float
    bathrooms: float
    floor_number: float
    base_price_egp: float
    expected_rent_monthly_egp: float
    price_per_sqm: float
    property_age: float
    rental_yield: float
    room_density: float
    popularity_score: float

class PropertyAnomalyResponse(BaseModel):
    model_name: str
    model_version: str
    anomaly_flag: int
    anomaly_score: float

class DailyCashFlowRecord(BaseModel):
    date: str
    net_cash_flow: float

class CashFlowForecastRequest(BaseModel):
    forecast_date: Optional[str] = None
    historical_series: Optional[List[DailyCashFlowRecord]] = None
    lag_1: Optional[float] = None
    lag_7: Optional[float] = None
    lag_14: Optional[float] = None
    lag_28: Optional[float] = None
    lag_30: Optional[float] = None
    rolling_mean_7: Optional[float] = None
    rolling_mean_14: Optional[float] = None
    rolling_mean_28: Optional[float] = None
    rolling_std_7: Optional[float] = None
    rolling_std_28: Optional[float] = None
    rolling_min_7: Optional[float] = None
    rolling_max_7: Optional[float] = None
    day_of_week: Optional[float] = None
    day_of_month: Optional[float] = None
    month: Optional[float] = None
    quarter: Optional[float] = None
    is_weekend: Optional[float] = None

class CashFlowForecastResponse(BaseModel):
    model_name: str
    model_version: str
    forecast_date: str
    predicted_net_cash_flow: float

class SegmentCustomerRecord(BaseModel):
    customer_id: str
    customer_type: str
    customer_tier: str
    budget_min_egp: float
    budget_max_egp: float
    monthly_income_egp: float
    interaction_frequency: str
    preferred_location: str
    preferred_property_type: str
