import json
import string
from typing import Optional, Dict, Any
import aiohttp
import os
from dotenv import load_dotenv

from pythonversus.user import User


class AsyncMvsAPIWrapper:
    def __init__(self, steam_token: Optional[str] = None):
        self.header: Optional[Dict[str, str]] = None
        self.token: Optional[str] = None
        self.steam_token: Optional[str] = None
        self.url: str = "https://dokken-api.wbagora.com/"
        self.session: Optional[aiohttp.ClientSession] = None

        if steam_token is None:
            load_dotenv()
            steam_token = os.getenv('MULTIVERSUS_TOKEN')

        self.steam_token = steam_token

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        await self.refresh_token()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def refresh_token(self, api_token: Optional[str] = None):
        if api_token is not None:
            self.steam_token = api_token

        temp_headers = {
            'x-hydra-api-key': '51586fdcbd214feb84b0e475b130fce0',
            'x-hydra-user-agent': 'Hydra-Cpp/1.132.0',
            'Content-Type': 'application/json',
            'x-hydra-client-id': '47201f31-a35f-498a-ae5b-e9915ecb411e'
        }
        temp_body = {"auth": {"fail_on_missing": 1, "steam": self.steam_token}, "options": ["wb_network"]}

        async with self.session.post(f"{self.url}access", json=temp_body, headers=temp_headers) as response:
            req = await response.json()
            self.token = req["token"]
            self.header = {
                'x-hydra-api-key': '51586fdcbd214feb84b0e475b130fce0',
                'x-hydra-user-agent': 'Hydra-Cpp/1.132.0',
                'Content-Type': 'application/json',
                'x-hydra-access-token': self.token
            }

    async def api_request(self, endpoint: str) -> Dict[str, Any]:
        async with self.session.get(endpoint, headers=self.header) as response:
            response.raise_for_status()
            return await response.json()

    async def get_player_profile(self, account_id: str) -> Dict[str, Any]:
        """
        Get the profile of a player using their account ID.
        """
        endpoint = f"{self.url}profiles/{account_id}"
        return await self.api_request(endpoint)

    async def get_player_account(self, account_id: str) -> Dict[str, Any]:
        """
        Get the account of a player using their account ID.
        """
        endpoint = f"{self.url}accounts/{account_id}"
        return await self.api_request(endpoint)

    async def get_id_from_username(self, account_name: str, limit: int = 5) -> str:
        """
        Perform a username search for a player. Tries to match the exact username.
        """
        endpoint = f"{self.url}profiles/search_queries/get-by-username/run?username={account_name}&limit={limit}"
        players = await self.api_request(endpoint)

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

    async def get_matches(self, account_id: str, count: Optional[int] = None) -> Dict[str, Any]:
        endpoint = f"{self.url}matches/all/{account_id}"
        if count is not None:
            endpoint += f"?count={count}"
        return await self.api_request(endpoint)

    async def get_most_recent_match(self, account_id: str) -> Dict[str, Any]:
        return await self.get_matches(account_id, 1)

    async def get_match_by_id(self, id: str) -> Dict[str, Any]:
        endpoint = f"{self.url}matches/{id}"
        return await self.api_request(endpoint)

    async def get_rank_data(self, account_id: str, gamemode: str, season: int = 2) -> Dict[str, Any]:
        endpoint = f"{self.url}leaderboards/ranked_season{season}_{gamemode}_all/score-and-rank/{account_id}"
        return await self.api_request(endpoint)


# Example usage
async def main():
    async with AsyncMvsAPIWrapper() as api:
        try:
            name = "taetae"
            user = await User.from_username(api, name)
            rank_str = await user.get_rank_str("2v2")
            print(name + "'s 2v2 rank: " + rank_str)
            # print("Username:", user.username)
            # print("id:", user.account_id)
            # print(json.dumps(user.profile_data))
        except aiohttp.ClientError as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())