from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass
from enum import Enum
if TYPE_CHECKING:
    from a_pythonversus import a_MvsAPI

class GameMode(Enum):
    ONE_VS_ONE_RANKED = "ranked-1v1"
    TWO_VS_TWO_RANKED = "ranked-2v2"
    # TODO: Double check these game modes
    ONE_VS_ONE = "1v1"
    TWO_VS_TWO = "2v2"
    FREE_FOR_ALL = "ffa"

@dataclass
class PlayerStats:
    account_id: str
    index: int
    username: str
    character: str
    damage_dealt: int
    damage_taken: int
    kills: int
    deaths: int
    assists: int
    rp_gain: Optional[int]
    rank: Optional[str]

@dataclass
class Match:
    """
    Represents a Match that has been played.
    """
    api: 'a_MvsAPI'
    match_id: Optional[str] = None
    raw_data: Optional[dict] = None
    mode: Optional[str] = None
    # TODO: Create Map class
    map: Optional[str] = None
    players: Optional[dict] = None
    score: Optional[list] = None
    winning_team_index: Optional[int] = None

    # Teams
    # Winner
    # Stats

    @classmethod
    async def from_id(cls, api: 'a_MvsAPI', match_id: str) -> 'Match':
        match = cls(api=api, match_id=match_id)
        await match.fetch_data()
        return match

    async def fetch_data(self):
        if not self.match_id:
            raise ValueError("No match_id provided")
        self.raw_data = await self.api.match_api.get_match_by_id(self.match_id)
        match_map = self.raw_data.get("server_data").get("GameplayConfig").get("Map")
        map_string = self.api.get_map_from_key(match_map)
        if map_string is None:
            self.map = match_map
        else:
            self.map = map_string
        # TODO: Add gamemode parser
        self.mode = self.raw_data.get("server_data").get("GameplayConfig").get("ModeString")
        # TODO: Parse players and teams somehow
        # self.players = self.raw_data.get("server_data").get()
        self.score = self.raw_data.get("players").get("all")[0].get("data").get("EndOfMatchStats").get("Score")
        self.winning_team_index = self.raw_data.get("players").get("all")[0].get("data").get("EndOfMatchStats").get("WinningTeamIndex")

class Match1v1(Match):
    pass


class Match2v2(Match):
    pass


class MatchFFA(Match):
    pass
