# Advanced Pydantic Usage Guide

## source [f17eabef18b38a70a38fb510130be58b](https://gist.github.com/shiningflash/f17eabef18b38a70a38fb510130be58b)

## Introduction

This guide explores advanced features of Pydantic, a powerful library for data validation and settings management in Python, leveraging type annotations. Aimed at enhancing backend development, it covers complex usage patterns, custom validation techniques, and integration strategies.

For basic user guide, follow the [official documentation](https://docs.pydantic.dev/latest/).

## Custom Validators

### Purpose

Enforce additional validation logic beyond type checks.

### Example

Validating an email field to contain a specific domain name.

```python
from pydantic import BaseModel, validator, EmailStr

class User(BaseModel):
    email: EmailStr

    @validator('email')
    def email_domain_validator(cls, v):
        if '@company-name.io' not in v:
            raise ValueError('Email must be on company-name.io domain')
        return v
```

## Recursive Models

### Purpose

For nested data structures, like trees or linked lists.

### Example

A category that can contain subcategories.

```python
from typing import List, Optional
from pydantic import BaseModel

class Category(BaseModel):
    name: str
    subcategories: Optional[List['Category']] = None

Category.update_forward_refs()
```

In the provided example, the `Category` model includes a field subcategories that is a list of `Category` objects. However, at the time `Category` is being defined, the `Category` class itself is not fully defined yet. By calling `Category.update_forward_refs()`, you instruct Pydantic to resolve the forward reference `List['Category']` to the actual `Category` class once it is fully defined.

## Generic Models

### Purpose

To create models that can work with different types.

### Example

A generic response model that can wrap any other Pydantic model.

```python
from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel, GenericModel

T = TypeVar('T')

class GenericResponse(GenericModel, Generic[T]):
    data: Optional[T] = None
    status: int
    message: str
    errors: Optional[List[str]] = None
    metadata: Optional[dict] = None

# Example model to use with the GenericResponse
class User(BaseModel):
    id: int
    name: str
    email: str

# Usage examples
# Successful response with data
successful_response = GenericResponse[User](
    data=User(id=1, name="Sakib Al Hasan", email="sakibalhasan@bcb.com"),
    status=200,
    message="Success",
)

# Response with error message and no data
error_response = GenericResponse[User](
    status=404,
    message="User not found",
    errors=["User with the given ID does not exist."]
)

# Response with pagination metadata
users_list = [
    User(id=1, name="Sakib Al Hasan", email="sakibalhasan@bcb.com"),
    User(id=2, name="Tamin Iqbal", email="tamimiqbal@bcb.com")
]
pagination_response = GenericResponse[List[User]](
    data=users_list,
    status=200,
    message="Success",
    metadata={"page": 1, "total_pages": 1, "per_page": 10, "total_items": 2}
)
```

## Settings Management with BaseSettings

### Purpose

For configuration data from environment variables.

### Example

Loading app settings with type validation.

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    debug_mode: bool = False
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
```

## Field Customization with Field

### Purpose

To provide additional validation and metadata for model fields.

### Example

Setting a default value, adding a title, and a description.

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., title="Item Name", description="The name of the item")
    quantity: int = Field(default=1, gt=0, description="Quantity of the item")
```

Here, `...` is used to mark a field as required.

## JSON Schema Customization

### Purpose

To customize the auto-generated JSON schema for models.

### Example

Adding examples to model fields for better documentation.

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(..., example="Sakib Al Hasan")
    age: int = Field(..., example=30)
```

## Dynamic Model Creation

### Purpose

To dynamically create models at runtime.

### Example

Creating a model based on runtime information.

```python
from pydantic import create_model

DynamicUser = create_model('DynamicUser',
                           id=(int, ...),
                           name=(str, ...),
                           email=(str, ...))

user = DynamicUser(id=123, name='Sakib Al Hasan', email='sakib@gmail.com')

# Access the model instance's attributes
print(user.id)     # Output: 123
print(user.name)   # Output: Sakib Al Hasan
print(user.email)  # Output: sakib@gmail.com

# Converting to a dictionary
user_dict = user.dict()
print(user_dict)  # Output: {'id': 123, 'name': 'Sakib Al Hasan', 'email': 'sakib@gmail.com'}

# Or converting to JSON
user_json = user.json()
print(user_json)  # Output: {"id": 123, "name": "Sakib Al Hasan", "email": "sakib@gmail.com"}
```

## ORM Mode

### Purpose

To simplify integration with ORMs like SQLAlchemy.

### Example

Converting an SQLAlchemy object to a Pydantic model.

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# Assuming user_orm is an instance from SQLAlchemy
# user_pydantic = User.from_orm(user_orm)
```

## Alias and Computed Properties

### Purpose

To use different field names in models and JSON representation or compute values.

### Example

Aliasing a model field and adding a computed field.

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    username: str = Field(..., alias='user_name')
    first_name: str
    last_name: str

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
```

## Union Types

### Purpose

To allow a field to accept multiple types.

### Example

A field that can be an int or a str.

```python
from typing import Union
from pydantic import BaseModel

class MixedTypeModel(BaseModel):
    mixed_field: Union[int, str]
```

# More Advanced Pydantic Usage Guide

## Custom Error Handling

### Purpose

To provide more informative error messages and handling mechanisms.

### Example

Customizing error handling for a more detailed response when validation fails.

```python
from pydantic import BaseModel, ValidationError, validator

class User(BaseModel):
    name: str
    age: int

    @validator('age')
    def check_age(cls, v):
        if v < 18:
            raise ValueError('Age must be at least 18')
        return v

try:
    User(name='Kabbya', age=17)
except ValidationError as e:
    print(e.json())
```

## Nested Validation

### Purpose

To validate data structures that include nested models.

### Example

Performing validation on a model that includes other models as fields.

```python
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    country: str

class Person(BaseModel):
    name: str
    address: Address

# This will validate both Person and Address instances
person = Person(name='Sakib Al Hasan', address={'city': 'Dhaka', 'country': 'Bangladesh'})
```

## Custom Types

### Purpose

To extend Pydantic's base type system with custom data types.

### Example

Creating a custom type for handling complex numbers.

```python
from pydantic import BaseModel
from pydantic.types import ConstrainedStr

class ComplexStr(ConstrainedStr):
    @classmethod
    def validate(cls, value):
        if not isinstance(value, str) or '+' not in value:
            raise ValueError('Invalid complex number format')
        return value

class ComplexNumberModel(BaseModel):
    complex_number: ComplexStr

model = ComplexNumberModel(complex_number='1+2j')
```

## Dependency Injection

### Purpose

To facilitate the injection of dependencies for models during instantiation.

### Example

Using dependency injection to provide a configuration object to models.

```python
from pydantic import BaseModel, Depends

def get_config():
    return {'config_key': 'config_value'}

class UsesConfig(BaseModel):
    config: dict = Depends(get_config)

model = UsesConfig()
print(model.config)
```