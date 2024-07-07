from pydantic import Field, field_serializer
from pydantic.alias_generators import to_camel

from datetime import date
from enum import Enum
from pydantic import BaseModel, ConfigDict
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


class ProductType(Enum):
    SOFTWARE = "software"
    ACCESSORIES = "accessories"
    HARDWARE = "hardware"
    COURSES = "courses"


data_json = """
{
    "product_id": "1234567890",
    "type": "hardware",
    "isReturnable": false,
    "completionDate": "2023-01-01",
    "msrpUSD": 93300,
    "manufacturer": "BMW",
    "number_of_components": 4,
    "code": "M4",
    "country_of_origin": "France" 
}
"""
# valid JSON does not allow trailing comma


class Automobile(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        str_strip_whitespace=True,
        validate_default=True,
        validate_assignment=True,
        alias_generator=to_camel,
    )
    product_id: str | int | None = None
    product_type: ProductType = Field(alias="type")
    is_returnable: bool = False
    manufactured_date: date = Field(validation_alias="completionDate")
    base_msrp_usd: float = Field(
        validation_alias="msrpUSD", serialization_alias="baseMSRPUSD"
    )
    number_of_components: int = Field(default=4, validation_alias="doors")
    code: str | None = None
    country_of_origin: str | None = None

    @field_serializer("manufactured_date", when_used="json-unless-none")
    def serialize_date(self, value: date) -> str:
        return value.strftime("%Y/%m/%d")


car = Automobile.model_validate_json(data_json)
console.print("\n[green]Python Object[/green]:")
console.print(car)
console.print("\n[blue]model_dump[/blue]:\n")
console.print(car.model_dump())
console.print("\n[yellow]model_dump alias=True[/]:\n")
console.print(car.model_dump(by_alias=True))
console.print("\n[cyan]model_dump_json alias=True[/]:\n")
console.print(car.model_dump_json(by_alias=True))
