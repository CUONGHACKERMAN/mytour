from enum import Enum

class TourStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"

class ServiceType(str, Enum):
    HOTEL = "HOTEL"
    TRANSFER = "TRANSFER"
    MEAL = "MEAL"
    ACTIVITY = "ACTIVITY"
    GUIDE = "GUIDE"
