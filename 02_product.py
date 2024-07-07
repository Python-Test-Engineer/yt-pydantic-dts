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
    sedan = "Sedan"
    coupe = "Coupe"
    HARDWARE = "hardware"
    suv = "SUV"
    truck = "Truck"


data_json = """
{
    "manufacturer": "BMW",
    "seriesName": "M4",
    "type": "hardware",
    "isElectric": false,
    "completionDate": "2023-01-01",
    "msrpUSD": 93300,
    "vin": "1234567890",
    "doors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB"
}
"""

expected_serialized_dict = {
    "manufacturer": "BMW",
    "series_name": "M4",
    "type_": ProductType.HARDWARE,
    "is_electric": False,
    "manufactured_date": date(2023, 1, 1),
    "base_msrp_usd": 93300.0,
    "vin": "1234567890",
    "number_of_doors": 2,
    "registration_country": "France",
    "license_plate": "AAA-BBB",
}


expected_serialized_dict_by_alias = {
    "manufacturer": "BMW",
    "seriesName": "M4",
    "type": ProductType.HARDWARE,
    "isElectric": False,
    "manufacturedDate": date(2023, 1, 1),
    "baseMSRPUSD": 93300.0,
    "vin": "1234567890",
    "numberOfDoors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB",
}


expected_serialized_json_by_alias = (
    '{"manufacturer":"BMW","seriesName":"M4","type":"hardware",'
    '"isElectric":false,"manufacturedDate":"2023/01/01","baseMSRPUSD":93300.0,'
    '"vin":"1234567890","numberOfDoors":2,"registrationCountry":"France",'
    '"licensePlate":"AAA-BBB"}'
)


class Automobile(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_default=True,
        validate_assignment=True,
        alias_generator=to_camel,
    )

    manufacturer: str
    series_name: str
    type_: ProductType = Field(alias="type")
    is_electric: bool = False
    manufactured_date: date = Field(validation_alias="completionDate")
    base_msrp_usd: float = Field(
        validation_alias="msrpUSD", serialization_alias="baseMSRPUSD"
    )
    vin: str
    number_of_doors: int = Field(default=4, validation_alias="doors")
    registration_country: str | None = None
    license_plate: str | None = None

    @field_serializer("manufactured_date", when_used="json-unless-none")
    def serialize_date(self, value: date) -> str:
        return value.strftime("%Y/%m/%d")


car = Automobile.model_validate_json(data_json)
console.print(car)
console.print(car.model_dump())
console.print(car.model_dump(by_alias=True))
console.print(car.model_dump_json(by_alias=True))
assert car.model_dump() == expected_serialized_dict

assert car.model_dump(by_alias=True) == expected_serialized_dict_by_alias

assert car.model_dump_json(by_alias=True) == expected_serialized_json_by_alias
