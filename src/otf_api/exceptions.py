import typing

if typing.TYPE_CHECKING:
    from httpx import Request, Response


class OtfError(Exception):
    """Base class for all exceptions in this package."""


class OtfRequestError(OtfError):
    """Raised when an error occurs while making a request to the OTF API."""

    original_exception: Exception | None
    response: "Response"
    request: "Request"

    def __init__(self, message: str, original_exception: Exception | None, response: "Response", request: "Request"):
        super().__init__(message)
        self.original_exception = original_exception
        self.response = response
        self.request = request


class RetryableOtfRequestError(OtfRequestError):
    """Raised when a request to the OTF API fails but can be retried.

    This is typically used for transient errors that may resolve on retry.
    """


class BookingError(OtfError):
    """Base class for booking-related errors, with an optional booking UUID attribute."""

    booking_uuid: str | None
    booking_id: str | None

    def __init__(self, message: str, booking_uuid: str | None = None, booking_id: str | None = None):
        super().__init__(message)
        self.booking_uuid = booking_uuid
        self.booking_id = booking_id


class AlreadyBookedError(BookingError):
    """Raised when attempting to book a class that is already booked."""


class ConflictingBookingError(BookingError):
    """Raised when attempting to book a class that conflicts with an existing booking."""


class BookingAlreadyCancelledError(BookingError):
    """Raised when attempting to cancel a booking that is already cancelled."""


class OutsideSchedulingWindowError(OtfError):
    """Raised when attempting to book a class outside the scheduling window."""


class ResourceNotFoundError(OtfError):
    """Raised when a resource is not found."""


class AlreadyRatedError(OtfError):
    """Raised when attempting to rate a class that is already rated."""


class ClassNotRatableError(OtfError):
    """Raised when attempting to rate a class that is not ratable."""
