from enum import Enum


class RouteKind(Enum):
    STREAM = 1
    MUSIC = 2
    REFERENCE = 3
    BOOKLET = 4
    STREAM_SET = 5
    MUSIC_SET = 6
    EDUCATION = 7


class ProductKind(Enum):
    BABY_LEAGUE = 3
    JUNIOR = 4
    TUTORING = 5
    JUNIOR_PLUS = 62
    JUNIOR_PLUS_LEVEL0 = 121
    JUNIOR_PLUS_LEVEL1 = 63
    JUNIOR_PLUS_LEVEL2 = 64
    JUNIOR_PLUS_LEVEL3 = 65
    JUNIOR_PLUS_MORE = 91
    SPECIAL_CLASS = 103
    COMMON = 120


class ContentGroup(Enum):
    SING = 3
    DANCE = 4
    SING_DANCE = 102
    PLUS_1_STORY = 85 
    PLUS_1_ACTION = 86 
    PLUS_1_DRAMA = 87 
    PLUS_1_LETTER = 88 
    PLUS_2_STORY = 89 
    PLUS_2_TWEET = 90 
    PLUS_2_DRAMA = 91 
    PLUS_2_SOUND = 92 
    PLUS_3_STORY = 93 
    PLUS_3_TALKING = 94 
    PLUS_3_DRAMA = 95 
    PLUS_3_RHYME = 96 

class BookletKind(Enum):
    STORY_BOOK = 117
    IMAGINATION_CANVAS = 118
    EXTRA_MATERIAL = 119


class BoardKind(Enum):
    REFERENCE = 105
    EXPERIENCE = 106
    CONSULT = 107
    NOTICE = 104
    SPECIAL = 103
    MOMS_CLASS = 110
    CLASS_NEW = 111
    CLASS_SPECIAL = 112
    EDU_CONSULT = 114
