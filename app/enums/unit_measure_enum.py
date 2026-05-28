from enum import Enum

class UnitMeasure(str, Enum):
    UNIT = "UN"
    KILOGRAM = "KG" 
    LITER = "LT"
    BOX = "CX"
    PACKAGE = "PCT"