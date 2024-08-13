from a_pythonversus.a_User import User

game_modes = ["2v2", "1v1", ]
from typing import TYPE_CHECKING
from dataclasses import dataclass
if TYPE_CHECKING:
    from a_pythonversus import a_MvsAPI

@dataclass
class Match:
    """
    Represents a Match that has been played.
    """
    api: 'a_MvsAPI'
    match_id: str
    raw_data: dict[str]
    mode: str
    # TODO: Create Map class
    map: str
    teams: list[User]
    isRanked: 'bool'

    @classmethod
    async def from_id(cls, api: 'a_MvsAPI', match_id: str) -> 'Match':
        match = cls(api=api, match_id=match_id)
        await match.fetch_data()
        return match

    async def fetch_data(self):
        if not self.match_id:
            raise ValueError("No match_id provided")
        self.raw_data = self.api.match_api.get_match_by_id(self.match_id)

class Match1v1(Match):
    pass


class Match2v2(Match):
    pass


class MatchFFA(Match):
    pass
