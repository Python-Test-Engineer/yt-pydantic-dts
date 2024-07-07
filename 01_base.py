from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from rich.console import Console
from pyboxen import boxen

console = Console()


output = """
We may have an API request that gives field names that are in no particular case format.
We need to create aliases to correspond with this and then create serialization aliases.
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


class Person(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, extra="forbid"
    )

    id_: int = Field(
        alias="id", default=1
    )  # Non-nulable but optional as value has default
    first_name: str | None = None  # Nullable and Optional as value has default
    last_name: str  # Required and non-nullable - must be str
    age: int | None = None  # Nullable and Optional as value has


p = Person(id=2, first_name="Isaac", lastName="Newton", age=84)


output = "Content goes here"
output += f"\n{p}"
print("\n")
print(
    boxen(
        output,
        title="Pydantic, [black on cyan] Fields [/]",
        subtitle="Cool subtitle goes here",
        subtitle_alignment="center",
        color="yellow",
        padding=1,
    )
)
console.print(f"{p}\n")


data_json = """
{
    "id": 3,
    "firstName": "Isaac",
    "last_name": "Newton",
    "age": 84
}
"""

p = Person.model_validate_json(data_json)

console.print(p)

console.print(p.model_dump())

console.print(p.model_dump(by_alias=True))

console.print(p.model_dump_json(by_alias=True))
