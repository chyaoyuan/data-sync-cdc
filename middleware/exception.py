class MiddlewareException(Exception):
    def __init__(self, message: str, **kwargs):
        self.message = message
        self.json_kwargs = kwargs
        super().__init__(message)
