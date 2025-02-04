class AuthTokenInvalidException(Exception):
    @property
    def message(self):
        return "Токен недействительный!"


class AuthTokenExpiredException(AuthTokenInvalidException):
    @property
    def message(self):
        return "Время жизни токена истекло!"
