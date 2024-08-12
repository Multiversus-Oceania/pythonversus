from dataclasses import dataclass
from typing import Optional, Dict, Any

from pythonversus import utils


@dataclass
class User:
    pythonversus: 'MvsAPIWrapper'
    account_id: Optional[str] = None
    username: Optional[str] = None
    profile_data: Optional[Dict[str, Any]] = None
    account_data: Optional[Dict[str, Any]] = None
    rank_data: Optional[Dict[str, Any]] = None

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

    async def get_rank_data(self, gamemode: str) -> Dict[str, Any]:
        rank_data = await self.pythonversus.get_rank_data(self.account_id, gamemode)
        self.rank_data = rank_data
        return rank_data

    async def get_elo(self, gamemode: str) -> float:
        rank_data = await self.get_rank_data(gamemode)
        elo = rank_data["score"]
        return elo

    async def get_rank_str(self, gamemode: str) -> str:
        return utils.elo_to_rank(await self.get_elo(gamemode))

    def __post_init__(self):
        if not self.pythonversus:
            raise ValueError("MvsAPIWrapper instance is required")
