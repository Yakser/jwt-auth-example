import enum


class Errors(enum.Enum):
    USER_DEACTIVATED = 'This user has been deactivated'
    WRONG_CREDENTIALS = 'Wrong username and/or password'