from .SalesItemServiceError import SalesItemServiceError


class DatabaseError(SalesItemServiceError):
    def __init__(self, error: Exception):
        super().__init__(
            500,
            'Internal Server Error',
            'Database error',
            'DatabaseError',
            '',
            error,
        )
