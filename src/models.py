from enum import Enum


class InfractionRecency(Enum):
    """
    How recently the last offense occurred.
    """
    TODAY_OR_YESTERDAY = -35
    PAST_WEEK = -20
    TWO_WEEKS_CLEAN = 15
    ONE_MONTH_CLEAN = 30


class InfractionSeverity(Enum):
    """
    The magnitude of the last offense.
    """
    NONE = 0
    MILD = -10
    MEDIUM = -25
    NUCLEAR = -50  


class ForgivenessStatus(Enum):
    """
    Mom's current emotional resolution of the past incident.
    """
    ACTIVE_COLD_WAR = -30   
    CAUTIOUS_TRUCE = -10    
    FULL_AMNESTY = 25       