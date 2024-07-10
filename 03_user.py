from uuid import uuid4
from pydantic import Field, field_serializer, UUID4, PastDate
from pydantic.alias_generators import to_camel
from datetime import date
from enum import Enum
from pydantic import BaseModel, ConfigDict
from rich.console import Console
from pyboxen import boxen
import requests

# https://docs.pydantic.dev/latest/api/types/
console = Console()
users = requests.get("https://dummyjson.com/users/3").json()
console.print(users)
console.print(type(users))
# output = """
# A User class with UUID type.
# When we use mutalbe dates or uuid in Model defintion, we need to use a factory instance as using regular pointer to data or uuid will create the value at compile time and will alwasy be the same.
# """
# print("\n")
# print(
#     boxen(
#         output,
#         title="Unclean API to Python fields and out as JSON",
#         # subtitle="-",
#         subtitle_alignment="center",
#         color="yellow",
#         padding=1,
#     )
# )

# data_json = """
# {
#     "user_id": "c0d4cbdf-60b6-4c82-8a2d-e340992f92a5",
#     "date_of_birth": "2000-01-01"
# }
# """
# # valid JSON does not allow trailing comma


# class User(BaseModel):
#     model_config = ConfigDict(
#         alias_generator=to_camel,  # camel case for
#         populate_by_name=True,  # allow pythonic field names as input
#         str_strip_whitespace=True,
#         validate_default=True,  # our defaults are not validated by default
#         validate_assignment=True,  # assignments are not validated by default
#         extra="allow",
#     )

#     user_id: int | str | UUID4 = Field(alias="id", default_factory=uuid4)
#     date_of_birth: date = Field(
#         alias="dateOfBirth",
#         default_factory=date.fromisoformat,
#     )
#     email: str = "unkown@unknown.com"


# user = User.model_validate_json(data_json)
# console.print("\n[green]Python Object[/green]:\n")
# console.print(user)
# console.print("\n[blue]model_dump[/blue]:\n")
# console.print(user.model_dump())
# console.print("\n[yellow]model_dump alias=True[/]:\n")
# console.print(user.model_dump(by_alias=True))
# console.print("\n[cyan]model_dump_json alias=True[/]:\n")
# console.print(user.model_dump_json(by_alias=True))

# print("\n\n\n")

# u = User(date_of_birth="2000-01-01")
# console.print(u)
