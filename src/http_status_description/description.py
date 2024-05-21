from enum import StrEnum


class HTTPResponseDescription(StrEnum):
    BAD_NUMBER = 'This number is already existing, try another one'
    NON_EXISTENT_NUMBER = 'This number is not in the system'
