from fastapi.responses import JSONResponse

class DomainError(Exception):

    status_code = 400
    default_message = "Bad Request"

    def __init__(
        self,
        message: str = None,
        data = None
    ):

        super().__init__(message)

        self.message = (
            message or self.default_message
        )

        self.data = data

    def to_dict(self):

        response = {
            "message": self.message
        }

        if self.data is not None:
            response["data"] = self.data

        return JSONResponse(response, self.status_code)

class BadRequest(DomainError):

    status_code = 400
    default_message = "Bad request."


class Unauthorized(DomainError):

    status_code = 401
    default_message = "Unauthorized."


class Forbidden(DomainError):

    status_code = 403
    default_message = "Forbidden."


class NotFound(DomainError):

    status_code = 404
    default_message = "Resource not found."


class MethodNotAllowed(DomainError):

    status_code = 405
    default_message = "Method not allowed."


class Conflict(DomainError):

    status_code = 409
    default_message = "Conflict."


class UnprocessableEntity(DomainError):

    status_code = 422
    default_message = "Unprocessable entity."


class TooManyRequests(DomainError):

    status_code = 429
    default_message = "Too many requests."


class InternalServerError(DomainError):

    status_code = 500
    default_message = "Internal server error."


class NotImplementedErrorHTTP(DomainError):

    status_code = 501
    default_message = "Not implemented."


class BadGateway(DomainError):

    status_code = 502
    default_message = "Bad gateway."


class ServiceUnavailable(DomainError):

    status_code = 503
    default_message = "Service unavailable."


class GatewayTimeout(DomainError):

    status_code = 504
    default_message = "Gateway timeout."