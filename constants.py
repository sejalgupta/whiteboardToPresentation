# class syntax
from enum import Enum

class SlideLayouts(Enum):
    TITLE_SLIDE = 0
    TITLE_AND_CONTENT_SLIDE = 1
    SECTION_HEADER = 2
    TWO_CONTENT = 3
    COMPARISON = 4
    TITLE_ONLY = 5
    BLANK = 6
    CONTENT_WITH_CAPTION = 7
    PICTURE_WITH_CAPTION = 8

layout_mapping = {
    "TITLE_SLIDE": SlideLayouts.TITLE_SLIDE,
    "TITLE_AND_CONTENT_SLIDE": SlideLayouts.TITLE_AND_CONTENT_SLIDE,
    "COMPARISON": SlideLayouts.COMPARISON,
    "TWO_CONTENT": SlideLayouts.TWO_CONTENT,
    "SECTION_HEADER": SlideLayouts.SECTION_HEADER,
    "TITLE_ONLY": SlideLayouts.TITLE_ONLY,
    "BLANK": SlideLayouts.BLANK,
    "CONTENT_WITH_CAPTION": SlideLayouts.CONTENT_WITH_CAPTION,
    "PICTURE_WITH_CAPTION": SlideLayouts.PICTURE_WITH_CAPTION
}