from flask import jsonify

class SuccessResponse:

    status_code = 200

    def __init__(
        self,
        message: str = "OK",
        data = None
    ):

        self.message = message
        self.data = data

    def to_response(self):

        response = {
            "message": self.message
        }

        if self.data is not None:
            response["data"] = self.data

        return jsonify(response), self.status_code
    

class OK(SuccessResponse):

    status_code = 200


class Created(SuccessResponse):

    status_code = 201


class Accepted(SuccessResponse):

    status_code = 202


class NoContent(SuccessResponse):

    status_code = 204