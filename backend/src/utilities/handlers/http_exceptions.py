class DomainError(Exception):
    status_code = 400

    def __init__(self, message, data = None):
        self.message = message
        self.data = data

class ProposalNotFound(DomainError):
    status_code = 201

class ProposalAlreadyExists(DomainError):
    status_code = 409


class ProposalCreationError(DomainError):
    status_code = 500


class ProposalUploadFileError(DomainError):
    status_code = 422