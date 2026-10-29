from dataclasses import dataclass
from models import (InfractionRecency, InfractionSeverity, ForgivenessStatus
                    , ChoreStatus, MomEnergy, RecentFriction,
                    AcademicStanding, CrowdFactor, LogisticsPlan
)

DEFAULT_BASE_SCORE: int = 50
MIN_SCORE: int = 0
MAX_SCORE: int = 100


@dataclass(frozen=True)
class TrustAssessment:
    score: int
    plan: str
    card_class: str
    verdict: str


def evaluate_plan(
    plan: str,
    recency: InfractionRecency,
    severity: InfractionSeverity,
    forgiveness: ForgivenessStatus,
    energy: MomEnergy,
    friction: RecentFriction,
    chores: ChoreStatus,
    crowd: CrowdFactor,
    academics: AcademicStanding,
    logistics: LogisticsPlan,
    base_score: int = DEFAULT_BASE_SCORE,
) -> TrustAssessment:
    """
    Calculates clamped final odds and returns the result.
    """

    recency_delta = recency.value if severity != InfractionSeverity.NONE else 0
    raw = (
        base_score
        + recency_delta
        + severity.value
        + forgiveness.value
        + energy.value
        + friction.value
        + chores.value
        + crowd.value
        + academics.value
        + logistics.value
    )

    final_score = max(MIN_SCORE, min(MAX_SCORE, raw))

    if final_score >= 70:
        card_class = "comic-green"
        verdict = "Chances are high. Go ask right now before she finds something to be mad about."
    elif final_score >= 40:
        card_class = "comic-yellow"
        verdict = "Risky 50/50. If you don't have a guaranteed ride or your chores done, sort that out first."
    else:
        card_class = "comic-red"
        verdict = f"Do not bring up '{plan}'. Stay in your room and stay quiet."

    return TrustAssessment(
        score=final_score,
        plan=plan,
        card_class=card_class,
        verdict=verdict,
    )