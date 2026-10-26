import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from src.models import ForgivenessStatus, InfractionRecency, InfractionSeverity
from src.trust_engine import evaluate_plan


def test_standard_penalties():
    # 50 - 35 (today) - 25 (medium) - 10 (truce) = -20 -> clamped to 0
    result = evaluate_plan(
        plan="Go to party",
        recency=InfractionRecency.TODAY_OR_YESTERDAY,
        severity=InfractionSeverity.MEDIUM,
        forgiveness=ForgivenessStatus.CAUTIOUS_TRUCE,
    )
    assert result.score == 0
    assert result.card_class == "comic-red"


def test_clean_streak_max_trust():
    # 50 + 30 (month clean) - 10 (mild) + 25 (amnesty) = 95
    result = evaluate_plan(
        plan="Hang out at the mall",
        recency=InfractionRecency.ONE_MONTH_CLEAN,
        severity=InfractionSeverity.MILD,
        forgiveness=ForgivenessStatus.FULL_AMNESTY,
    )
    assert result.score == 95
    assert result.card_class == "comic-green"


def test_score_clamped_at_upper_bound():
    # 80 base + 30 (month clean) + 25 (amnesty) = 135 -> clamped to 100
    result = evaluate_plan(
        plan="Borrow the car",
        recency=InfractionRecency.ONE_MONTH_CLEAN,
        severity=InfractionSeverity.MILD,
        forgiveness=ForgivenessStatus.FULL_AMNESTY,
        base_score=80,
    )
    assert result.score == 100
    assert result.card_class == "comic-green"


def test_nuclear_disaster_clamps_to_zero():
    # 50 - 35 (today) - 50 (nuclear) - 30 (cold war) = -65 -> clamped to 0
    result = evaluate_plan(
        plan="Ask for pocket money",
        recency=InfractionRecency.TODAY_OR_YESTERDAY,
        severity=InfractionSeverity.NUCLEAR,
        forgiveness=ForgivenessStatus.ACTIVE_COLD_WAR,
    )
    assert result.score == 0
    assert result.card_class == "comic-red"