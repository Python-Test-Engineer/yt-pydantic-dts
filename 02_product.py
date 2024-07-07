from pydantic import Field, field_serializer
from pydantic.alias_generators import to_camel

from datetime import date
from enum import Enum
from pydantic import BaseModel, ConfigDict
from rich.console import Console
from pyboxen import boxen

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


class Product(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,  # camel case for
        populate_by_name=True,  # allow pythonic field names as input
        str_strip_whitespace=True,
        validate_default=True,  # our defaults are not validated by default
        validate_assignment=True,  # assignments are not validated by default
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

    # various options for 'when'
    # https://docs.pydantic.dev/latest/api/pydantic_core_schema/#pydantic_core.core_schema.WhenUsed
    @field_serializer("manufactured_date", when_used="json-unless-none")
    def serialize_date(self, value: date) -> str:
        return value.strftime("%Y/%m/%d")


product = Product.model_validate_json(data_json)
console.print("\n[green]Python Object[/green]:\n")
console.print(product)
console.print("\n[blue]model_dump[/blue]:\n")
console.print(product.model_dump())
console.print("\n[yellow]model_dump alias=True[/]:\n")
console.print(product.model_dump(by_alias=True))
console.print("\n[cyan]model_dump_json alias=True[/]:\n")
console.print(product.model_dump_json(by_alias=True))

print("\n\n\n")
