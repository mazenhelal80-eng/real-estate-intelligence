from typing import List
import pandas as pd
from fastapi import APIRouter, HTTPException

from backend.schemas.ml import (
    PricePredictionRequest,
    PricePredictionResponse,
    LeadConversionRequest,
    LeadConversionResponse,
    CustomerSegmentationRequest,
    CustomerSegmentationResponse,
    PropertyAnomalyRequest,
    PropertyAnomalyResponse,
    CashFlowForecastRequest,
    CashFlowForecastResponse,
    SegmentCustomerRecord,
)
from backend.ml_services.price_prediction import predict_property_price
from backend.ml_services.lead_conversion import predict_lead_conversion
from backend.ml_services.customer_segmentation import segment_customer, get_customers_by_segment
from backend.ml_services.property_anomaly import detect_property_anomaly
from backend.ml_services.cash_flow_forecast import forecast_cash_flow

router = APIRouter(prefix="/api/v1/ml", tags=["Machine Learning"])

@router.post("/price-prediction", response_model=PricePredictionResponse)
def predict_price(request: PricePredictionRequest):
    try:
        data = request.model_dump(by_alias=True)
        result = predict_property_price(data)
        return PricePredictionResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal ML service error")

@router.post("/lead-conversion", response_model=LeadConversionResponse)
def predict_conversion(request: LeadConversionRequest):
    try:
        data = request.model_dump(by_alias=True)
        result = predict_lead_conversion(data)
        return LeadConversionResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal ML service error")

@router.post("/customer-segmentation", response_model=CustomerSegmentationResponse)
def segment_customer_route(request: CustomerSegmentationRequest):
    try:
        data = request.model_dump(by_alias=True)
        result = segment_customer(data)
        return CustomerSegmentationResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal ML service error")

@router.get("/customer-segmentation/segments/{cluster_id}/customers", response_model=List[SegmentCustomerRecord])
def get_segment_customers(cluster_id: int, limit: int = 10):
    if cluster_id not in [0, 1, 2, 3]:
        raise HTTPException(status_code=400, detail="Invalid cluster_id. Must be between 0 and 3.")
    try:
        records = get_customers_by_segment(cluster_id, limit=limit)
        return [SegmentCustomerRecord(**r) for r in records]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve segment customers")

@router.post("/property-anomaly", response_model=PropertyAnomalyResponse)
def detect_anomaly_route(request: PropertyAnomalyRequest):
    try:
        data = request.model_dump(by_alias=True)
        result = detect_property_anomaly(data)
        return PropertyAnomalyResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal ML service error")

@router.post("/cash-flow-forecast", response_model=CashFlowForecastResponse)
def forecast_cash_flow_route(request: CashFlowForecastRequest):
    try:
        if request.historical_series is not None and len(request.historical_series) > 0:
            df = pd.DataFrame([r.model_dump() for r in request.historical_series])
            result = forecast_cash_flow(df, forecast_date=request.forecast_date)
        else:
            payload = request.model_dump(by_alias=True, exclude_none=True)
            result = forecast_cash_flow(payload, forecast_date=request.forecast_date)
        return CashFlowForecastResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal ML service error")
