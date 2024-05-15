class UserNotFoundException(Exception):
    detail = "user not found"


class UserNotAwailable(Exception):
    detail = "user credintals are not available"


class TokenExpireError(Exception):
    detail = "token in user jwt was expired"


class TokenNotValidError(Exception):
    detail = "Can not decode token. It's not correct!"
