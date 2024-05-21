import re
from typing import Annotated

from pydantic import BaseModel, Field
from pydantic.functional_validators import AfterValidator


def validate_phone(v: str) -> str:
    if not re.match(r'^(\+?[78])?[- ]?\(?\d{3}\)?[- ]?(\d{3})[- ]?(\d{2})[- ]?(\d{2})$', v):
        raise ValueError('Invalid phone number')
    # format number 7xxxxxxxxxx or 8xxxxxxxxxx
    phone_number = ''.join([number for number in list(v) if number not in '+()- '])

    # maybe another way: return '7' + phone_number[1:]
    return phone_number


class ClientData(BaseModel):
    phone: Annotated[str, AfterValidator(validate_phone)]
    address: str = Field(min_length=3)
