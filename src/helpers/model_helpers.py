from typing import Type, TypeVar

import pydantic
from asyncpg import Record

T = TypeVar("T")


class BaseModel(pydantic.BaseModel):
    @classmethod
    def parse_list(cls: Type[T], data: list[dict | Record]) -> list[T]:
        return [cls(**d) for d in data]

    @classmethod
    def parse_obj(cls: Type[T], data: dict | Record | None) -> T | None:
        return cls(**data)

    @classmethod
    def parse_tuple(cls: Type[T], data: list[dict | Record]) -> tuple[T, ...]:
        return tuple(cls(**d) for d in data)

    @classmethod
    def parse_set(cls: Type[T], data: list[dict | Record]) -> set[T]:
        return set(cls(**d) for d in data)
