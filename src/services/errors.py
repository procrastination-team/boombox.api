class ServiceError(Exception):
    pass


class BadTokenError(Exception):
    def __init__(self, message: str):
        description = f"Problems with auth token. {message}"
        super().__init__(description)
