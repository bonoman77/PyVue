from enum import Enum


class ChannelKind(Enum):
    TUNTUN = 1
    BABYLEAGUE = 2
    MASTERCLUB = 3
    PRESCHOOL = 4 
    LATTJR = 5 
    JUNIORPLUS = 77  
 

class SourceKind(Enum):
    SELF = 78
    EXPERIENCE = 79 
    FAIR = 80
    MOMS_CLASS = 81
    MOMS_DIARY = 82
    LEVEL_TEST = 83 


class RecordKind(Enum):
    CONSULT = 11
    SUPPORT = 12 
    VIOLATION = 13


class ReportKind(Enum):
    TUNTUN = 91
    MASTERCLUB = 92
    GROUP = 93
    PRESCHOOL = 94
    LATTJR = 95
    SOURCE = 96
    MASTERCLUB_ORDER = 101
    HEALTH = 102
    SCHEDULE = 103

