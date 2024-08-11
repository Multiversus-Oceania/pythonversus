from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class User:
    pythonversus: 'MvsAPIWrapper'
    account_id: Optional[str] = None
    username: Optional[str] = None
    profile_data: Optional[Dict[str, Any]] = None
    account_data: Optional[Dict[str, Any]] = None

    @classmethod
    async def from_id(cls, pythonversus: 'MvsAPIWrapper', account_id: str) -> 'User':
        user = cls(pythonversus=pythonversus, account_id=account_id)
        await user.fetch_data()
        return user

    @classmethod
    async def from_username(cls, pythonversus: 'MvsAPIWrapper', username: str) -> 'User':
        account_id = await pythonversus.get_id_from_username(username)
        return await cls.from_id(pythonversus, account_id)

    async def fetch_data(self) -> None:
        if not self.account_id:
            raise ValueError("Account ID is required to fetch data")

        self.account_data = await self.pythonversus.get_player_account(self.account_id)
        self.profile_data = await self.pythonversus.get_player_profile(self.account_id)
        self.username = self.account_data["identity"]["alternate"]["wb_network"][0]["username"]

    def __post_init__(self):
        if not self.pythonversus:
            raise ValueError("MvsAPIWrapper instance is required")
