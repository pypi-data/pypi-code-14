from ..web import HttpError


class JsonifyHttpError:
    def __call__(self, controller, next):
        try:
            next()
        except HttpError as e:
            response = controller.response
            response.status_code = e.status_code

            if not isinstance(e.description, str):
                response.json(e.description)
            else:
                response.body = e.description
                response.content_type = 'text/plain; charset=utf8'
