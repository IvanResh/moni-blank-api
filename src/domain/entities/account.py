from helpers import BaseModel


class AccountDb(BaseModel):
    id: int | None = None
    name: str | None = None
