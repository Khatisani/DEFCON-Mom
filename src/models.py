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

class MomEnergy(Enum):
    """
    Mom's current workload and vibe.
    """
    CHILLING = 15     
    STRESSED = -20  


class RecentFriction(Enum):
    """
    Did you clash recently?
    """
    NO_ARGUMENT = 0
    ARGUED_RECENTLY = -30  

class ChoreStatus(Enum):
    """
    Domestic audit and status of chores.
    """
    CHORES_DONE = 20     
    CHORES_UNDONE = -40

class CrowdFactor(Enum):
    """
    The people around you 
    """
    TRUSTED_ADULT = 30
    ALL_GIRLS = 10
    MIXED_GROUP = -20
    UNKNOWN_BOYS = -45


class AcademicStanding(Enum):
    """
    Academic factors such as very good report and poor performance 
    """
    RECENT_GOOD_MARKS = 20
    UPCOMING_EXAM = -40
    RECENT_BAD_MARKS = -40


class LogisticsPlan(Enum):
    """
    Travelling safety
    """
    RIDE_ARRANGED_EARLY = 15
    FIGURE_OUT_LATER = -35
