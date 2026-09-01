from app.models.insight import InsightResponse, InsightSeverity

class InsightService:
  """Generates actionable insights from processed telemetry data."""

  def generate_insight(
      self,
      *,
      device_id: str,
      metric: str,
      summary: str,
      recommendation: str,
      severity: InsightSeverity,
  ) -> InsightResponse:
      return InsightResponse(
         device_id=device_id,
         metric=metric,
         summary=summary,
         recommendation=recommendation,
         severity=severity,
      )

  def generate_from_anomaly(self, anomaly: dict) -> InsightResponse:
     device_id = anomaly["device_id"]
     metric = anomaly["metric"]
     classification = anomaly["classification"]

     if metric == "soil_moisture" and classification == "LOW":
        return self.generate_insight(
           device_id=device_id,
           metric=metric,
           summary="Soil moisture is below the configured threshold.",
           recommendation="Inspect irrigation and verify adequate water delivery.",
           severity="warning",
        )

     if metric == "soil_moisture" and classification == "HIGH":
        return self.generate_insight(
          device_id=device_id,
          metric=metric,
          summary="Soil moisture is above the configured threshold.",
          recommendation="Inspect drainage and irrigation if appropriate.",
          severity="warning", 
        )

     return self.generate_insight(
        device_id=device_id,
        metric=metric,
        summary=f"{metric} is operating within the expected range.",
        recommendation="Continue monitoring telemetry for changes.",
        severity="normal",
     )