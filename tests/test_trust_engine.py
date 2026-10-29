import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from src.models import (
    ChoreStatus,
    ForgivenessStatus,
    InfractionRecency,
    InfractionSeverity,
    MomEnergy,
    RecentFriction,
) 

from src.trust_engine import evaluate_plan

def test_perfect_scenario():
    # 50 + 30 (clean) + 25 (amnesty) + 15 (chilling) + 0 (no fight) + 20 (chores done) = 140 -> to 100
    res = evaluate_plan(
        plan="Go to mall",
        recency=InfractionRecency.ONE_MONTH_CLEAN,
        severity=InfractionSeverity.MILD,
        forgiveness=ForgivenessStatus.FULL_AMNESTY,
        energy=MomEnergy.CHILLING,
        friction=RecentFriction.NO_ARGUMENT,
        chores=ChoreStatus.CHORES_DONE,
    )
    assert res.score == 100
    assert res.card_class == "comic-green"

def test_undone_chores_and_argument_penalty():
    # 50 + 15 (2 weeks) - 10 (mild) + 25 (amnesty) - 20 (stressed) - 30 (argued) - 40 (chores undone) = -10 -> 0
    res = evaluate_plan(
        plan="Sleepover",
        recency=InfractionRecency.TWO_WEEKS_CLEAN,
        severity=InfractionSeverity.MILD,
        forgiveness=ForgivenessStatus.FULL_AMNESTY,
        energy=MomEnergy.STRESSED,
        friction=RecentFriction.ARGUED_RECENTLY,
        chores=ChoreStatus.CHORES_UNDONE,
    )
    assert res.score == 0
    assert res.card_class == "comic-red"

def test_green_zone_smooth_sailing():
    # Base 50 + 15 (2 weeks clean) - 10 (mild) + 25 (amnesty) + 15 (chilling) + 0 (no argument) + 20 (chores done)
    # Total = 115 -> clamped to 100
    res = evaluate_plan(
        plan="Go watch a movie",
        recency=InfractionRecency.TWO_WEEKS_CLEAN,
        severity=InfractionSeverity.MILD,
        forgiveness=ForgivenessStatus.FULL_AMNESTY,
        energy=MomEnergy.CHILLING,
        friction=RecentFriction.NO_ARGUMENT,
        chores=ChoreStatus.CHORES_DONE,
    )
    assert res.score == 100
    assert res.card_class == "comic-green"


def test_amber_zone_risky_gamble():
    # Base 50 - 20 (past week) - 25 (medium) + 25 (amnesty) + 15 (chilling) + 0 (no argument) + 20 (chores done)
    # Total = 65 -> Amber zone (40 <= score < 70)
    res = evaluate_plan(
        plan="Order pizza",
        recency=InfractionRecency.PAST_WEEK,
        severity=InfractionSeverity.MEDIUM,
        forgiveness=ForgivenessStatus.FULL_AMNESTY,
        energy=MomEnergy.CHILLING,
        friction=RecentFriction.NO_ARGUMENT,
        chores=ChoreStatus.CHORES_DONE,
    )
    assert res.score == 65
    assert res.card_class == "comic-yellow"


def test_red_zone_total_disaster():
    # Base 50 - 35 (today) - 50 (nuclear) - 30 (cold war) - 20 (stressed) - 30 (argued) - 40 (chores undone)
    # Total = -155 -> to 0
    res = evaluate_plan(
        plan="Go to a sleepover",
        recency=InfractionRecency.TODAY_OR_YESTERDAY,
        severity=InfractionSeverity.NUCLEAR,
        forgiveness=ForgivenessStatus.ACTIVE_COLD_WAR,
        energy=MomEnergy.STRESSED,
        friction=RecentFriction.ARGUED_RECENTLY,
        chores=ChoreStatus.CHORES_UNDONE,
    )
    assert res.score == 0
    assert res.card_class == "comic-red"

def test_perfect_scenario():
    # 50 + 30 (clean) + 25 (amnesty) + 15 (chilling) + 0 (no fight) + 20 (chores done) = 140 -> to 100
    res = evaluate_plan(
        plan="Go to mall",
        recency=InfractionRecency.ONE_MONTH_CLEAN,
        severity=InfractionSeverity.MILD,
        forgiveness=ForgivenessStatus.FULL_AMNESTY,
        energy=MomEnergy.CHILLING,
        friction=RecentFriction.NO_ARGUMENT,
        chores=ChoreStatus.CHORES_DONE,
    )
    assert res.score == 100
    assert res.card_class == "comic-green"


def test_undone_chores_and_argument_penalty():
    # 50 + 15 (2 weeks) - 10 (mild) + 25 (amnesty) - 20 (stressed) - 30 (argued) - 40 (chores undone) = -10 -> 0
    res = evaluate_plan(
        plan="Sleepover",
        recency=InfractionRecency.TWO_WEEKS_CLEAN,
        severity=InfractionSeverity.MILD,
        forgiveness=ForgivenessStatus.FULL_AMNESTY,
        energy=MomEnergy.STRESSED,
        friction=RecentFriction.ARGUED_RECENTLY,
        chores=ChoreStatus.CHORES_UNDONE,
    )
    assert res.score == 0
    assert res.card_class == "comic-red"

def test_amber_zone_risky_gamble():
    # Base 50 - 20 (past week) - 25 (medium) + 25 (amnesty) + 15 (chilling) + 0 (no argument) + 20 (chores done)
    # Total = 65 -> Amber zone (40 <= score < 70)
    res = evaluate_plan(
        plan="Order pizza",
        recency=InfractionRecency.PAST_WEEK,
        severity=InfractionSeverity.MEDIUM,
        forgiveness=ForgivenessStatus.FULL_AMNESTY,
        energy=MomEnergy.CHILLING,
        friction=RecentFriction.NO_ARGUMENT,
        chores=ChoreStatus.CHORES_DONE,
    )
    assert res.score == 65
    assert res.card_class == "comic-yellow"

