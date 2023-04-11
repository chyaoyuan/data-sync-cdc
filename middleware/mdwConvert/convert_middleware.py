from middleware.mdwConvert.convert.application import get_convert_app


class ConvertMiddleware:
    def __init__(self):
        self.convert = get_convert_app()