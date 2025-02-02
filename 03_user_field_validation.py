from uuid import uuid4
from pydantic import (
    Field,
    field_serializer,
    UUID4,
    PastDate,
    field_validator,
    ValidationError,
)
from pydantic.alias_generators import to_camel
from datetime import date
from enum import Enum
from pydantic import BaseModel, ConfigDict
from rich.console import Console
from pyboxen import boxen
import requests
from rich.traceback import install

# classes start LINE 110
install(show_locals=True)
# using the following api
URL = "https://dummyjson.com/users/3"

# we get:
user_dict = {
    "id": 3,
    "firstName": "Sophia",
    "lastName": "Brown",  # errors for < 3, lower case firt letter and first letter c or C
    "maidenName": "",
    "age": "42",
    "gender": "female",
    "email": "sophia.brown@x.dummyjson.com",
    "phone": "+81 210-652-2785",
    "username": "sophiab",
    "password": "sophiabpass",
    "birthDate": "1982-11-6",
    "image": "https://dummyjson.com/icon/sophiab/128",
    "bloodGroup": "O-",
    "height": 177.72,
    "weight": 52.6,
    "eyeColor": "Hazel",
    "hair": {"color": "White", "type": "Wavy"},
    "ip": "214.225.51.195",
    "address": {
        "address": "1642 Ninth Street",
        "city": "Washington",
        "state": "Alabama",
        "stateCode": "AL",
        "postalCode": "32822",
        "coordinates": {"lat": 45.289366, "lng": 46.832664},
        "country": "United States",
    },
    "macAddress": "12:a3:d3:6f:5c:5b",
    "university": "Pepperdine University",
    "bank": {
        "cardExpire": "04/25",
        "cardNumber": "7795895470082859",
        "cardType": "Korean Express",
        "currency": "SEK",
        "iban": "90XYKT83LMM7AARZ8JN958JC",
    },
    "company": {
        "department": "Research and Development",
        "name": "Schiller - Zieme",
        "title": "Accountant",
        "address": {
            "address": "1896 Washington Street",
            "city": "Dallas",
            "state": "Nevada",
            "stateCode": "NV",
            "postalCode": "88511",
            "coordinates": {"lat": 20.086743, "lng": -34.577107},
            "country": "United States",
        },
    },
    "ein": "963-113",
    "ssn": "638-461-822",
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)  Chrome/96.0.4664.45 Safari/537.36",
    "crypto": {
        "coin": "Bitcoin",
        "wallet": "0xb9fc2fe63b2a6c003f1c324c3bfa53259162181a",
        "network": "Ethereum (ERC20)",
    },
    "role": "admin",
}
# https://docs.pydantic.dev/latest/api/types/
console = Console()
users = requests.get(URL).json()
console.print(users)
console.print(type(users))
output = """
We can apply a range of before and after validators to a field. The ordering is specified in the case of multiple validators for a particular field.
"""
print("\n")
print(
    boxen(
        output,
        title="Unclean API to Python fields and out as JSON",
        # subtitle="-",
        subtitle_alignment="center",
        color="yellow",
        padding=1,
    )
)


class User(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,  # camel case for
        populate_by_name=True,  # allow pythonic field names as input
        str_strip_whitespace=True,
        validate_default=True,  # our defaults are not validated by default
        validate_assignment=True,  # assignments are not validated by default
        extra="ignore",  # ignore extra fields
    )

    user_id: int | str | UUID4 = Field(alias="id")
    first_name: str
    last_name: str
    age: int
    email: str

    # we can add many fields to a given validator, so we could use @field_validator("last_name, "first_name") etc
    @field_validator("last_name")
    @classmethod
    def after_validator_1(cls, value):
        print("after_validator_1_nearest")
        if len(value) < 3:
            # we use ValueError to raise an exception and Pydantic will catch it
            raise ValueError("After Validator: last_name must be at least 3 characters")
        return value

    @field_validator("last_name")
    @classmethod
    def after_validator_2(cls, value):
        print("after_validator_2")
        if value[0] != value[0].upper():
            # we use ValueError to raise an exception and Pydantic will catch it
            raise ValueError("Last name must start with an uppercase letter")
        return value

    @field_validator("last_name")
    @classmethod
    def after_validator_3(cls, value):
        print("after_validator_3_furthest_away")
        if value[0].lower() == "c":
            # we use ValueError to raise an exception and Pydantic will catch it
            raise ValueError("Last name must not start with c insensitive case")

        return value.upper()

    @field_validator("last_name", mode="before")
    @classmethod
    def before_validator_1(cls, value):
        print("before_validator_1_nearest")
        if len(value) < 3:
            # we use ValueError to raise an exception and Pydantic will catch it
            raise ValueError(
                "Before Validator: last_name must be at least 3 characters"
            )
        return value

    @field_validator("last_name", mode="before")
    @classmethod
    def before_validator_2(cls, value):
        print("before_validator_2")
        return value

    @field_validator("last_name", mode="before")
    @classmethod
    def before_validator_3(cls, value):
        print("before_validator_3_furthest_away")
        return value


user = User.model_validate(user_dict)
console.print("\n[green]Python Object[/green]:\n")
console.print(user)
console.print("\n[blue]model_dump[/blue]:\n")
console.print(user.model_dump())
console.print("\n[yellow]model_dump alias=True[/]:\n")
console.print(user.model_dump(by_alias=True))
console.print("\n[cyan]model_dump_json alias=True[/]:\n")
console.print(user.model_dump_json(by_alias=True))
console.print("\n[purple4]model_dump_json alias=False[/]:\n")
console.print(user.model_dump_json(by_alias=False))

print("\n")
