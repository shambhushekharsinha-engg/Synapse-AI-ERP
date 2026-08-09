import numpy as np
from typing import List, Dict
from app.schemas.supplier_intelligence import (
    SupplierScoreResponse, SupplierLeadTimeAnalytics, 
    SupplierDelayRiskResponse, SupplierComparisonProduct
)

class SupplierIntelligenceService:
    @staticmethod
    def calculate_supplier_score(
        supplier_id: int,
        on_time_rate: float,
        avg_lead_time_days: float,
        delay_rate: float
    ) -> SupplierScoreResponse:
        """
        Calculates a deterministic supplier performance score.
        Weighted: 60% on-time, 30% low delay rate, 10% competitive lead time (baseline 5 days).
        """
        # A simple scoring algorithm for the MVP
        score_on_time = on_time_rate * 100
        score_delay = max(0, 100 - (delay_rate * 100 * 2)) # Heavily penalize delays
        
        # Lead time score: assuming 5 days is a perfect 100
        lt_score = max(0, 100 - ((max(0, avg_lead_time_days - 5)) * 5))
        
        final_score = (score_on_time * 0.6) + (score_delay * 0.3) + (lt_score * 0.1)
        
        if final_score >= 90:
            rating = "EXCELLENT"
        elif final_score >= 80:
            rating = "GOOD"
        elif final_score >= 60:
            rating = "FAIR"
        else:
            rating = "POOR"
            
        return SupplierScoreResponse(
            supplier_id=supplier_id,
            score=round(final_score, 1),
            rating=rating,
            on_time_rate=round(on_time_rate, 2),
            avg_lead_time_days=round(avg_lead_time_days, 1),
            delay_rate=round(delay_rate, 2)
        )

    @staticmethod
    def calculate_lead_time_analytics(
        supplier_id: int,
        historical_lead_times: List[float],
        delay_frequency: float
    ) -> SupplierLeadTimeAnalytics:
        if not historical_lead_times:
            return SupplierLeadTimeAnalytics(
                supplier_id=supplier_id,
                average_lead_time=0.0,
                median_lead_time=0.0,
                standard_deviation=0.0,
                minimum=0.0,
                maximum=0.0,
                delay_frequency=delay_frequency
            )
            
        return SupplierLeadTimeAnalytics(
            supplier_id=supplier_id,
            average_lead_time=round(float(np.mean(historical_lead_times)), 2),
            median_lead_time=round(float(np.median(historical_lead_times)), 2),
            standard_deviation=round(float(np.std(historical_lead_times)), 2),
            minimum=round(float(np.min(historical_lead_times)), 2),
            maximum=round(float(np.max(historical_lead_times)), 2),
            delay_frequency=round(delay_frequency, 2)
        )

    @staticmethod
    def evaluate_delay_risk(
        supplier_id: int,
        delay_frequency: float,
        lead_time_variance: float,
        lead_time_trend: str # e.g., "INCREASING", "STABLE", "DECREASING"
    ) -> SupplierDelayRiskResponse:
        risk_factors = []
        
        if delay_frequency > 0.15:
            risk_factors.append("High historical delay frequency")
            
        if lead_time_variance > 5.0:
            risk_factors.append("High lead time variability")
            
        if lead_time_trend == "INCREASING":
            risk_factors.append("Lead time is trending upward")
            
        if len(risk_factors) >= 2:
            risk_level = "HIGH"
        elif len(risk_factors) == 1:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
            
        return SupplierDelayRiskResponse(
            supplier_id=supplier_id,
            risk_level=risk_level,
            risk_factors=risk_factors
        )
