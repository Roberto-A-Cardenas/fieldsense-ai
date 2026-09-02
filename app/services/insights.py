from app.db.models import TelemetryRecord
from app.models.insight import InsightResponse, InsightSeverity
from app.services.ai_provider import AIProvider
from app.services.anomaly import detect_anomaly


class InsightService:
  """Generates actionable insights from processed telemetry data.
  """

  def __init__(
            self,
            ai_provider: AIProvider | None = None,
    ):
            self.ai_provider = ai_provider

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

  def generate_from_anomaly(
          self, 
          anomaly: dict,
      ) -> InsightResponse:
          device_id = anomaly["device_id"]
          metric = anomaly["metric"]
          classification = anomaly["classification"]

          if metric == "soil_moisture" and classification == "LOW":
              fallback = self.generate_insight(
               device_id=device_id,
               metric=metric,
               summary="Soil moisture is below the configured threshold.",
               recommendation="Inspect irrigation and verify adequate water delivery.",
               severity="warning",
           )

          elif metric == "soil_moisture" and classification == "HIGH":
           fallback = self.generate_insight(
            device_id=device_id,
            metric=metric,
            summary="Soil moisture is above the configured threshold.",
            recommendation="Inspect drainage and irrigation if appropriate.",
            severity="warning",
           )
          else:
            fallback = self.generate_insight(
             device_id=device_id,
             metric=metric,
             summary=f"{metric} is operating within the expected range.",
             recommendation="Continue monitoring telemetry for changes.",
             severity="normal",
           )

          if self.ai_provider is None:
              return fallback

          return self.ai_provider.generate_insight(
              anomaly=anomaly,
              fallback=fallback,
            )

  def generate_from_reading(
        self,
        reading: TelemetryRecord,
    ) -> InsightResponse:
        anomaly = detect_anomaly(reading)

        return self.generate_from_anomaly(anomaly)