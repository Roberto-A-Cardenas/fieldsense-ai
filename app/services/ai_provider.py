from abc import ABC, abstractmethod

from app.models.insight import InsightResponse


class AIProvider(ABC):
  """Interface for AI-backed insight generation."""

  @abstractmethod
  def generate_insight(
    self,
    *,
    anomaly: dict,
    fallback: InsightResponse,
) -> InsightResponse:
    """Generate an AI-enhanced insight."""
    raise NotImplementedError