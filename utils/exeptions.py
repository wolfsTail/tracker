class UserNotFoundException(Exception):
    detail = "user not found"


class UserNotAwailable(Exception):
    detail = "user credintals are not available"
