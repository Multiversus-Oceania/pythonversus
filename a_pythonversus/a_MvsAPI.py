import json
from typing import Optional, Dict, Any
import aiohttp
import os
from dotenv import load_dotenv

from a_pythonversus.a_MatchAPI import MatchAPI
from a_pythonversus.a_User import User
from a_pythonversus.a_Character import CharacterManager, Character
from a_pythonversus.a_UserAPI import UserAPI


class a_MvsAPIWrapper:
    def __init__(self, steam_token: Optional[str] = None):
        self.header: Optional[Dict[str, str]] = None
        self.token: Optional[str] = None
        self.steam_token: Optional[str] = None
        self.url: str = "https://dokken-api.wbagora.com/"
        self.session: Optional[aiohttp.ClientSession] = None

        # API Helpers
        self.character_manager = CharacterManager('characters.json')
        self.user_api = UserAPI(self)
        self.match_api = MatchAPI(self)

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

    # API Utils
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

    async def request(self, endpoint: str) -> Dict[str, Any]:
        async with self.session.get(self.url + endpoint, headers=self.header) as response:
            response.raise_for_status()
            return await response.json()

    # User lookup
    async def get_user_from_username(self, username: str) -> Optional[User]:
        user = await User.from_username(self, username)
        return user if user is not None else None

    async def get_user_from_id(self, account_id: str) -> Optional[User]:
        user = await User.from_id(self, account_id)
        return user if user is not None else None

    @staticmethod
    def get_character_by_slug(self, slug: str) -> Optional['Character']:
        return self.character_manager.get_character_by_slug(slug)

    @staticmethod
    def get_character_from_key(self, key: str) -> Optional['Character']:
        return self.character_manager.get_character_by_key(key)

    @staticmethod
    def get_character_from_name(self, name: str) -> Optional['Character']:
        return self.character_manager.get_character_by_name(name)

    async def custom_request(self, endpoint: str) -> Dict[str, Any]:
        """
        Perform a GET request to a given endpoint on the MultiVersus API
        """
        return await self.request(endpoint)


# Example usage
async def main():
    async with a_MvsAPIWrapper() as api:
        try:
            name = "taetae"
            user = await User.from_username(api, name)
            recent_match_id = await user.get_most_recent_match_id()
            # recent_match = await api.match_api.get_match_by_id("66b5d4afec0f1df34e87dd83")
            # print(json.dumps(recent_match, indent=4))
            print(recent_match_id)
        except aiohttp.ClientError as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
