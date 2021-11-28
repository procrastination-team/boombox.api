class ServiceError(Exception):
    pass


class BadTokenError(ServiceError):
    def __init__(self, reason: str):
        description = f"Problems with auth token. {reason}"
        super().__init__(description)
