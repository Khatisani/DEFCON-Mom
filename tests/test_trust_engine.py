import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from models import (
    ChoreStatus,
    ForgivenessStatus,
    InfractionRecency,
    InfractionSeverity,
    MomEnergy,
    RecentFriction,
    AcademicStanding,
    CrowdFactor,
    LogisticsPlan,
    )
from trust_engine import evaluate_plan


def test_perfect_scenario():
    # 50 + 30 (month clean) + 0 (none) + 25 (amnesty) + 15 (chilling) + 0 (no argument) + 20 (chores)
    # + 30 (trusted adult) + 20 (good marks) + 15 (ride arranged) = 205 -> to 100
    res = evaluate_plan(
        plan="Go to mall",
        recency=InfractionRecency.ONE_MONTH_CLEAN,
        severity=InfractionSeverity.NONE,
        forgiveness=ForgivenessStatus.FULL_AMNESTY,
        energy=MomEnergy.CHILLING,
        friction=RecentFriction.NO_ARGUMENT,
        chores=ChoreStatus.CHORES_DONE,
        crowd=CrowdFactor.TRUSTED_ADULT,
        academics=AcademicStanding.RECENT_GOOD_MARKS,
        logistics=LogisticsPlan.RIDE_ARRANGED_EARLY,
    )
    assert res.score == 100
    assert res.card_class == "comic-green"


def test_green_zone_smooth_sailing():
    # 50 + 15 (2 weeks clean) - 10 (mild) + 25 (amnesty) + 15 (chilling) + 0 (no argument) + 20 (chores done)
    # + 10 (all girls) + 20 (good marks) + 15 (ride arranged) = 160 -> to 100
    res = evaluate_plan(
        plan="Go watch a movie",
        recency=InfractionRecency.TWO_WEEKS_CLEAN,
        severity=InfractionSeverity.MILD,
        forgiveness=ForgivenessStatus.FULL_AMNESTY,
        energy=MomEnergy.CHILLING,
        friction=RecentFriction.NO_ARGUMENT,
        chores=ChoreStatus.CHORES_DONE,
        crowd=CrowdFactor.ALL_GIRLS,
        academics=AcademicStanding.RECENT_GOOD_MARKS,
        logistics=LogisticsPlan.RIDE_ARRANGED_EARLY,
    )
    assert res.score == 100
    assert res.card_class == "comic-green"


def test_amber_zone_risky_gamble():
    # 50 - 20 (past week) - 25 (medium) + 25 (amnesty) + 15 (chilling) + 0 (no argument) + 20 (chores done)
    # - 20 (mixed group) + 20 (good marks) - 35 (figure out lift later) = 50 -> Amber zone (40-69)
    res = evaluate_plan(
        plan="Order pizza",
        recency=InfractionRecency.PAST_WEEK,
        severity=InfractionSeverity.MEDIUM,
        forgiveness=ForgivenessStatus.FULL_AMNESTY,
        energy=MomEnergy.CHILLING,
        friction=RecentFriction.NO_ARGUMENT,
        chores=ChoreStatus.CHORES_DONE,
        crowd=CrowdFactor.MIXED_GROUP,
        academics=AcademicStanding.RECENT_GOOD_MARKS,
        logistics=LogisticsPlan.FIGURE_OUT_LATER,
    )
    assert res.score == 50
    assert res.card_class == "comic-yellow"


def test_undone_chores_and_argument_penalty():
    # 50 + 15 (2 weeks) - 10 (mild) + 25 (amnesty) - 20 (stressed) - 30 (argued) - 40 (chores undone)
    # - 20 (mixed group) - 40 (upcoming exam) - 35 (lift later) = -135 -> to 0
    res = evaluate_plan(
        plan="Sleepover",
        recency=InfractionRecency.TWO_WEEKS_CLEAN,
        severity=InfractionSeverity.MILD,
        forgiveness=ForgivenessStatus.FULL_AMNESTY,
        energy=MomEnergy.STRESSED,
        friction=RecentFriction.ARGUED_RECENTLY,
        chores=ChoreStatus.CHORES_UNDONE,
        crowd=CrowdFactor.MIXED_GROUP,
        academics=AcademicStanding.UPCOMING_EXAM,
        logistics=LogisticsPlan.FIGURE_OUT_LATER,
    )
    assert res.score == 0
    assert res.card_class == "comic-red"


def test_red_zone_total_disaster():
    # 50 - 35 (today) - 50 (nuclear) - 30 (cold war) - 20 (stressed) - 30 (argued) - 40 (chores undone)
    # - 45 (unknown boys) - 40 (upcoming exam) - 35 (lift later) = -275 -> to 0
    res = evaluate_plan(
        plan="Go to a sleepover",
        recency=InfractionRecency.TODAY_OR_YESTERDAY,
        severity=InfractionSeverity.NUCLEAR,
        forgiveness=ForgivenessStatus.ACTIVE_COLD_WAR,
        energy=MomEnergy.STRESSED,
        friction=RecentFriction.ARGUED_RECENTLY,
        chores=ChoreStatus.CHORES_UNDONE,
        crowd=CrowdFactor.UNKNOWN_BOYS,
        academics=AcademicStanding.UPCOMING_EXAM,
        logistics=LogisticsPlan.FIGURE_OUT_LATER,
    )
    assert res.score == 0
    assert res.card_class == "comic-red"