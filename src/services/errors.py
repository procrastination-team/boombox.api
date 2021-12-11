class ServiceError(Exception):
    pass


class BadTokenError(ServiceError):
    def __init__(self, reason: str):
        description = f"Problems with auth token. {reason}"
        super().__init__(description)


class BadRequestError(ServiceError):
    def __init__(self, message: str):
        super().__init__(message)
