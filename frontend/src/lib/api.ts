import {
  CashFlowForecastRequest,
  CashFlowForecastResponse,
  CustomerSegmentationRequest,
  CustomerSegmentationResponse,
  HealthResponse,
  LeadConversionRequest,
  LeadConversionResponse,
  PricePredictionRequest,
  PricePredictionResponse,
  PropertyAnomalyRequest,
  PropertyAnomalyResponse,
  SegmentCustomerRecord,
} from "@/types/api";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

async function fetchJson<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    },
  });

  if (!response.ok) {
    let errorDetail = "API request failed";
    try {
      const errorJson = await response.json();
      errorDetail = errorJson.detail || JSON.stringify(errorJson);
    } catch {
      errorDetail = `Status ${response.status}: ${response.statusText}`;
    }
    throw new Error(errorDetail);
  }

  return response.json();
}

export async function checkHealth(): Promise<HealthResponse> {
  return fetchJson<HealthResponse>("/health");
}

export async function predictPropertyPrice(data: PricePredictionRequest): Promise<PricePredictionResponse> {
  return fetchJson<PricePredictionResponse>("/api/v1/ml/price-prediction", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function predictLeadConversion(data: LeadConversionRequest): Promise<LeadConversionResponse> {
  return fetchJson<LeadConversionResponse>("/api/v1/ml/lead-conversion", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function segmentCustomer(data: CustomerSegmentationRequest): Promise<CustomerSegmentationResponse> {
  return fetchJson<CustomerSegmentationResponse>("/api/v1/ml/customer-segmentation", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getCustomersBySegment(clusterId: number, limit: number = 10): Promise<SegmentCustomerRecord[]> {
  return fetchJson<SegmentCustomerRecord[]>(`/api/v1/ml/customer-segmentation/segments/${clusterId}/customers?limit=${limit}`);
}

export async function detectPropertyAnomaly(data: PropertyAnomalyRequest): Promise<PropertyAnomalyResponse> {
  return fetchJson<PropertyAnomalyResponse>("/api/v1/ml/property-anomaly", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function forecastCashFlow(data: CashFlowForecastRequest): Promise<CashFlowForecastResponse> {
  return fetchJson<CashFlowForecastResponse>("/api/v1/ml/cash-flow-forecast", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
