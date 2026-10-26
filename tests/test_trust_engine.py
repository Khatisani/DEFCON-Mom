from src.models import InfractionRecency, InfractionSeverity, ForgivenessStatus
from src.trust_engine import calculate_base_trust


def test_standard_penalties():
    result = calculate_base_trust(
        recency=InfractionRecency.TODAY_OR_YESTERDAY,
        severity=InfractionSeverity.MEDIUM,
        forgiveness=ForgivenessStatus.CAUTIOUS_TRUCE,
    )
    assert result.raw_score == -20
    assert result.final_score == 0


def test_clean_streak_max_trust():
    result = calculate_base_trust(
        recency=InfractionRecency.ONE_MONTH_CLEAN,
        severity=InfractionSeverity.MILD,
        forgiveness=ForgivenessStatus.FULL_AMNESTY,
    )
    assert result.raw_score == 95
    assert result.final_score == 95


def test_score_clamped_at_upper_bound():
    result = calculate_base_trust(
        recency=InfractionRecency.ONE_MONTH_CLEAN,
        severity=InfractionSeverity.MILD,
        forgiveness=ForgivenessStatus.FULL_AMNESTY,
        starting_score=80,
    )
    assert result.raw_score == 125
    assert result.final_score == 100


def test_nuclear_disaster_clamps_to_zero():
    result = calculate_base_trust(
        recency=InfractionRecency.TODAY_OR_YESTERDAY,
        severity=InfractionSeverity.NUCLEAR,
        forgiveness=ForgivenessStatus.ACTIVE_COLD_WAR,
    )
    assert result.raw_score == -65
    assert result.final_score == 0