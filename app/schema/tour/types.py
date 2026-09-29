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

class TourBoundaryType(str, Enum):
    DOMESTIC = "DOMESTIC"
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"
    CROSS_BORDER = "CROSS_BORDER"

