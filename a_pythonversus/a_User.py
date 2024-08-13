from dataclasses import dataclass
from typing import Optional, Dict, Any, TYPE_CHECKING

from a_pythonversus import Utils

if TYPE_CHECKING:
    from a_pythonversus import a_MvsAPI


@dataclass
class User:
    pythonversus: 'a_MvsAPI'
    account_id: Optional[str] = None
    username: Optional[str] = None
    profile_data: Optional[Dict[str, Any]] = None
    account_data: Optional[Dict[str, Any]] = None

    @classmethod
    async def from_id(cls, pythonversus: 'a_MvsAPI', account_id: str) -> 'User':
        user = cls(pythonversus=pythonversus, account_id=account_id)
        await user.fetch_data()
        return user

    @classmethod
    async def from_username(cls, pythonversus: 'a_MvsAPI', username: str) -> 'User':
        account_id = await pythonversus.user_api.get_id_from_username(username)
        return await cls.from_id(pythonversus, account_id)

    async def fetch_data(self) -> None:
        if not self.account_id:
            raise ValueError("Account ID is required to fetch data")

        self.account_data = await self.pythonversus.user_api.get_player_account(self.account_id)
        self.profile_data = await self.pythonversus.user_api.get_player_profile(self.account_id)
        self.username = self.account_data["identity"]["alternate"]["wb_network"][0]["username"]

    async def refresh_profile(self):
        self.profile_data = await self.pythonversus.user_api.get_player_profile(self.account_id)

    # Rank Information
    async def get_rank_data(self, account_id: str, gamemode: str, character: str = "all", season: int = 2) -> Dict[
        str, Any]:
        endpoint = f"leaderboards/ranked_season{season}_{gamemode}_{character}/score-and-rank/{account_id}"
        return await self.pythonversus.user_api.request(endpoint)

    # async def get_highest_ranked_character(self, gamemode: str) -> ''

    async def get_elo(self, gamemode: str, character: str = "all") -> float:
        rank_data = await self.get_rank_data(gamemode, character)
        elo = rank_data["score"]
        return elo

    async def get_rank_str(self, gamemode: str, character: str = "all") -> str:
        return Utils.elo_to_rank(await self.get_elo(gamemode, character))

    async def get_most_recent_match(self):
        return await self.pythonversus.match_api.get_matches(self.account_id, 1)

    def __post_init__(self):
        if not self.pythonversus:
            raise ValueError("MvsAPIWrapper instance is required")
