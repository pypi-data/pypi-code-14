from django.http import HttpResponse


class RESTDispatch:
    """ Handles passing on the request to the correct view method based on the request type.
    """
    def run(self, *args, **named_args):
        request = args[0]
        if "GET" == request.META['REQUEST_METHOD']:
            if hasattr(self, "GET"):
                return self.GET(*args, **named_args)
            else:
                return invalid_method()
        elif "POST" == request.META['REQUEST_METHOD']:
            if hasattr(self, "POST"):
                return self.POST(*args, **named_args)
            else:
                return invalid_method()
        elif "PUT" == request.META['REQUEST_METHOD']:
            if hasattr(self, "PUT"):
                return self.PUT(*args, **named_args)
            else:
                return invalid_method()
        elif "DELETE" == request.META['REQUEST_METHOD']:
            if hasattr(self, "DELETE"):
                return self.DELETE(*args, **named_args)
            else:
                return invalid_method()

        else:
            return invalid_method()


def invalid_method():
    response = HttpResponse("Method not allowed")
    response.status_code = 405
    return response

