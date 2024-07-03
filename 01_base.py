import uuid
from datetime import date
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    PlainValidator,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    WrapValidator,
    EmailStr,
    validator,
)
from pydantic.functional_validators import field_validator
from rich.console import Console
import pyboxen


console = Console()


class User(BaseModel):
    user_id: uuid.UUID = uuid.uuid4()
    first_name: str
    last_name: str
    birthdate: date
    email: EmailStr
    address_1: str
    address_2: str | None = None
    city: str
    state: str | None = None
    postcode: str


@field_validator("first_name", "last_name")
def validate_name(cls, first, last):
    if len(first) < 3:
        raise ValueError("First name must be at least 3 characters.")
    if len(last) < 3:
        raise ValueError("Last name must be at least 3 characters.")
    return first, last


user = User(
    first_name="",
    last_name="Doe",
    birthdate=date(1990, 1, 1),
    email="john.doe@example.com",
    address_1="123 Main St",
    city="New York",
    postcode="10001",
)

user = User.model_validate(user)

console.print(user)
