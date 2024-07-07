from uuid import uuid4
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
A Prodcut class with nested Enum class.
We have set model level alias to camel case. and feilds are overwritten.
As we are using alias in the ConfigDict, we use validation_alias for input aliases on fields and we also use serialization aliases for output.
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

user_id = uuid4()
data_json = """
{
    "email": "jane.doe@example.com",
    "date_of_birth": "2000-01-01"
}
"""
# valid JSON does not allow trailing comma


class User(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,  # camel case for
        populate_by_name=True,  # allow pythonic field names as input
        str_strip_whitespace=True,
        validate_default=True,  # our defaults are not validated by default
        validate_assignment=True,  # assignments are not validated by default
        extra="allow",
    )
    user_id: UUID4 = Field(
        alias="id", default_factory=uuid4
    )  # fields created at compile time so will always reference just one 'instance'
    email: str
    # date_of_birth: date = Field(
    #     alias="dateOfBirth",
    #     default_factory=date.fromisoformat,
    # )

    # various options for 'when'
    # https://docs.pydantic.dev/latest/api/pydantic_core_schema/#pydantic_core.core_schema.WhenUsed


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
