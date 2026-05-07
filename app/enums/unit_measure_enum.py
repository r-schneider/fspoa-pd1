from enum import Enum

class UnitMeasture(str, Enum):
    UNIT = "UN"
    KILOGRAM = "KG" 
    LITER = "LT"
    BOX = "CX"
    PACKAGE = "PCT"