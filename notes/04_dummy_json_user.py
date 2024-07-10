from uuid import uuid4
import json
from pydantic import Field, field_serializer, UUID4, PastDate
from pydantic.alias_generators import to_camel
from datetime import date
from enum import Enum
from pydantic import BaseModel, ConfigDict
from rich.console import Console
from pyboxen import boxen


# https://docs.pydantic.dev/latest/api/types/
console = Console()

output = """
A User class with UUID type.
When we use mutalbe dates or uuid in Model defintion, we need to use a factory instance as using regular pointer to data or uuid will create the value at compile time and will alwasy be the same.
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
# https://dummyjson.com/docs/users#users-single
data_json = """
{
    "id": 1,
    "firstName": "Emily",
    "lastName": "Johnson",
    "maidenName": "Smith",
    "age": 28,
    "gender": "female",
    "email": "emily.johnson@x.dummyjson.com",
    "phone": "+81 965-431-3024",
    "username": "emilys",
    "password": "emilyspass",
    "birthDate": "1996-5-30",
    "image": "...",
    "bloodGroup": "O-",
    "height": 193.24,
    "weight": 63.16,
    "eyeColor": "Green",
    "hair": {
        "color": "Brown",
        "type": "Curly"
    },
    "ip": "42.48.100.32",
    "address": {
        "address": "626 Main Street",
        "city": "Phoenix",
        "state": "Mississippi",
        "stateCode": "MS",
        "postalCode": "29112",
        "coordinates": {
            "lat": -77.16213,
            "lng": -92.084824
        },
        "country": "United States"
    },
    "macAddress": "47:fa:41:18:ec:eb",
    "university": "University of Wisconsin--Madison",
    "bank": {
        "cardExpire": "03/26",
        "cardNumber": "9289760655481815",
        "cardType": "Elo",
        "currency": "CNY",
        "iban": "YPUXISOBI7TTHPK2BR3HAIXL"
    },
    "company": {
        "department": "Engineering",
        "name": "Dooley, Kozey and Cronin",
        "title": "Sales Manager",
        "address": {
            "address": "263 Tenth Street",
            "city": "San Francisco",
            "state": "Wisconsin",
            "stateCode": "WI",
            "postalCode": "37657",
            "coordinates": {
                "lat": 71.814525,
                "lng": -161.150263
            },
            "country": "United States"
        }
    },
    "ein": "977-175",
    "ssn": "900-590-289",
    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
    "crypto": {
        "coin": "Bitcoin",
        "wallet": "0xb9fc2fe63b2a6c003f1c324c3bfa53259162181a",
        "network": "Ethereum (ERC20)"
    },
    "role": "admin"
}
"""


class User(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,  # camel case for
        populate_by_name=True,  # allow pythonic field names as input
        str_strip_whitespace=True,
        validate_default=True,  # our defaults are not validated by default
        validate_assignment=True,  # assignments are not validated by default
        extra="ignore",  # ignore extra fields
    )

    user_id: int | str | UUID4 = Field(alias="id", default_factory=uuid4)
    date_of_birth: str | None = Field(alias="birthDate")
    email: str = "unkown@unknown.com"
    first_name: str
    last_name: str
    age: int
    address: dict


user = User.model_validate_json(data_json)
console.print("\n[green]Python Object[/green]:\n")
console.print(user)
console.print("\n[blue]model_dump[/blue]:\n")
console.print(user.model_dump())
console.print("\n[yellow]model_dump alias=True[/]:\n")
console.print(user.model_dump(by_alias=True))
console.print("\n[cyan]model_dump_json alias=True[/]:\n")
console.print(user.model_dump_json(by_alias=True))

print("\n\n\n")
