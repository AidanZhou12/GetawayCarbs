from enum import Enum

class OrderType(str, Enum):
    DINE_IN = "dine-in"
    TAKEOUT = "takeout"
    PICKUP = "pickup"