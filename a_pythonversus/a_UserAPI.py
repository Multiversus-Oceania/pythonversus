from typing import Dict, Any, TYPE_CHECKING
if TYPE_CHECKING:
    from a_pythonversus import a_MvsAPI


class UserAPI:
    def __init__(self, api: 'a_MvsAPI'):
        self.api = api

    async def get_player_profile(self, account_id: str) -> Dict[str, Any]:
        """
        Get the profile of a player using their account ID.
        """
        endpoint = f"profiles/{account_id}"
        return await self.api.request(endpoint)
    
    async def get_player_account(self, account_id: str) -> Dict[str, Any]:
        """
        Get the account of a player using their account ID.
        """
        endpoint = f"accounts/{account_id}"
        return await self.api.request(endpoint)

    async def get_id_from_username(self, account_name: str, limit: int = 5) -> str:
        """
        Perform a username search for a player. Tries to match the exact username.
        """
        endpoint = f"profiles/search_queries/get-by-username/run?username={account_name}&limit={limit}"
        players = await self.api.request(endpoint)

        search_length = len(players["results"])

        if search_length == 1:
            return players["results"][0]["result"]["account_id"]
        else:
            for player in players["results"]:
                account_id = player["result"]["account_id"]
                account_data = await self.get_player_account(account_id)
                username = account_data["identity"]["alternate"]["wb_network"][0]["username"]
                if username and username.lower() == account_name.lower():
                    return account_id

        return "Failed to find matching account"

    async def get_username_from_id(self, account_id: str) -> str:
        account_data = await self.get_player_account(account_id)
        username = account_data["identity"]["alternate"]["wb_network"][0]["username"]
        return username if username else "Failed to find matching account"

