class ClassNotFoundError(Exception):
    """Raised when a fitness class is not found"""
    pass

class NoSlotsAvailableError(Exception):
    """Raised when no slots are available for a class"""
    pass

class DuplicateBookingError(Exception):
    """Raised when a client tries to book the same class twice"""
    pass