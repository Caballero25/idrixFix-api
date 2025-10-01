class DomainError(Exception):
    """Excepción base de dominio."""


class NotFoundError(DomainError):
    pass


class AlreadyExistsError(DomainError):
    pass


class ValidationError(DomainError):
    pass


class RepositoryError(DomainError):
    """Error genérico si no encaja en las anteriores."""

    pass
