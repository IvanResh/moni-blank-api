from enum import Enum
from typing import Type

import marshmallow
from marshmallow import fields, validate


class Schema(marshmallow.Schema):
    class Meta:
        ordered = True


class EnumField(fields.String):
    """Deserializes strings into enum objects and serializes them back to
    strings."""

    enum_cls: Type[Enum]
    validator: validate.Validator

    def __init__(self, enum_cls: Type[Enum], /, **kwargs) -> None:
        self.validate = validate.OneOf([x.value for x in enum_cls])
        super().__init__(**kwargs, validate=self.validate)
        self.enum_cls = enum_cls

    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        return self.enum_cls(self.validate(value))

    def _serialize(self, value, attr, obj, **kwargs):
        value = value.value if value else None
        return super()._serialize(value, attr, obj, **kwargs)


class OrderByDirection(str, Enum):
    DESC = "DESC"
    ASC = "ASC"
