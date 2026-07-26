from enum import Enum

class OrderType(str, Enum):
    DINE_IN = "Dine In"
    TAKEOUT = "Takeout"
    PICKUP = "Pickup"