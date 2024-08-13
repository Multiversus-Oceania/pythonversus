from typing import Dict, Any, TYPE_CHECKING, Optional

from a_pythonversus.a_User import User

if TYPE_CHECKING:
    from a_pythonversus import a_MvsAPI


class MatchAPI:
    def __init__(self, api: 'a_MvsAPI'):
        self.api = api

    async def get_matches(self, account_id: str, count: Optional[int] = None) -> Dict[str, Any]:
        endpoint = f"matches/all/{account_id}"
        if count is not None:
            endpoint += f"?count={count}"
        return await self.api.request(endpoint)

    async def get_match_by_id(self, match_id: str) -> Dict[str, Any]:
        endpoint = f"matches/{match_id}"
        return await self.api.request(endpoint)
