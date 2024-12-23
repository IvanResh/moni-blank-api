from domain import AccountNotFoundException, AccountRepository
from helpers import BaseModel


class GetAccountQuery(BaseModel):
    id: int


class GetAccountResponse(BaseModel):
    id: int
    name: str


class GetAccountHandler:

    def __init__(self, account_repository: AccountRepository) -> None:
        self._account_repository = account_repository

    async def handle(self, query: GetAccountQuery) -> GetAccountResponse:
        account = await self._account_repository.get_account_by_id(id=query.id)
        if not account:
            raise AccountNotFoundException()

        return GetAccountResponse(
            id=account["id"],
            name=account["name"],
        )
