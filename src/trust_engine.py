from dataclasses import dataclass
from models import InfractionRecency, InfractionSeverity, ForgivenessStatus

DEFAULT_BASE_SCORE: int = 50
MIN_SCORE: int = 0
MAX_SCORE: int = 100


@dataclass(frozen=True)
class TrustBreakdown:
    starting_score: int
    recency_delta: int
    severity_delta: int
    forgiveness_delta: int
    raw_score: int
    final_score: int


def calculate_base_trust(
    recency: InfractionRecency,
    severity: InfractionSeverity,
    forgiveness: ForgivenessStatus,
    starting_score: int = DEFAULT_BASE_SCORE,
) -> TrustBreakdown:
    """
    Calculates the clamped base trust score (0-100) and returns an audit breakdown.
    """
    
    recency_delta = recency.value if severity != InfractionSeverity.NONE else 0
    severity_delta = severity.value
    forgiveness_delta = forgiveness.value

    raw_score = starting_score + recency_delta + severity_delta + forgiveness_delta
    final_score = max(MIN_SCORE, min(MAX_SCORE, raw_score))

    return TrustBreakdown(
        starting_score=starting_score,
        recency_delta=recency_delta,
        severity_delta=severity_delta,
        forgiveness_delta=forgiveness_delta,
        raw_score=raw_score,
        final_score=final_score,
    )