#!/usr/bin/python3
import json
from typing import Optional, Dict, Any
import aiohttp
import os
from dotenv import load_dotenv

from a_pythonversus.a_Match import Match
from a_pythonversus.a_MatchAPI import MatchAPI
from a_pythonversus.a_User import User
from a_pythonversus.character import CharacterManager, Character
from a_pythonversus.a_UserAPI import UserAPI


class MvsAPIWrapper:
    """
    A wrapper for the MultiVersus API.

    This class provides methods to interact with the MultiVersus API,
    including user lookup, character management, and match data retrieval.

    :param steam_token: Optional Steam token for authentication.
    :type steam_token: Optional[str]
    """

    def __init__(self, steam_token: Optional[str] = None):
        """
        Initialize the MvsAPIWrapper.

        :param steam_token: Optional Steam token for authentication.
        :type steam_token: Optional[str]
        """
        self.header: Optional[Dict[str, str]] = None
        self.token: Optional[str] = None
        self.steam_token: Optional[str] = self._get_steam_token(steam_token)
        self.url: str = "https://dokken-api.wbagora.com/"
        self.session: Optional[aiohttp.ClientSession] = None

        # API Helpers
        self.character_manager = CharacterManager('characters.json')
        self.user_api = UserAPI(self)
        self.match_api = MatchAPI(self)

        self.maps = self._load_maps()

    @staticmethod
    def _get_steam_token(steam_token: Optional[str]) -> Optional[str]:
        """
        Get the Steam token from the provided parameter or environment variable.

        :param steam_token: Steam token provided during initialization.
        :type steam_token: Optional[str]
        :return: Steam token.
        :rtype: Optional[str]
        """
        if steam_token is None:
            load_dotenv()
            return os.getenv('MULTIVERSUS_TOKEN')
        return steam_token

    @staticmethod
    def _load_maps() -> Dict[str, Any]:
        """
        Load map data from a JSON file.

        :return: Dictionary containing map data.
        :rtype: Dict[str, Any]
        """
        with open('maps.json', 'r') as f:
            return json.load(f)

    async def __aenter__(self):
        """
        Async context manager entry point.

        :return: Self instance.
        :rtype: MvsAPIWrapper
        """
        self.session = aiohttp.ClientSession()
        await self.refresh_token()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Async context manager exit point.

        :param exc_type: Exception type if an exception was raised.
        :param exc_val: Exception value if an exception was raised.
        :param exc_tb: Exception traceback if an exception was raised.
        """
        await self.session.close()

    async def refresh_token(self, api_token: Optional[str] = None):
        """
        Refresh the API access token.

        :param api_token: Optional API token to use instead of the stored Steam token.
        :type api_token: Optional[str]
        """
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
        """
        Make a GET request to the specified API endpoint.

        :param endpoint: API endpoint to request.
        :type endpoint: str
        :return: JSON response from the API.
        :rtype: Dict[str, Any]
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        async with self.session.get(self.url + endpoint, headers=self.header) as response:
            response.raise_for_status()
            return await response.json()

    async def get_user_from_username(self, username: str) -> Optional[User]:
        """
        Get a User object from a username.

        :param username: Username to look up.
        :type username: str
        :return: User object if found, None otherwise.
        :rtype: Optional[User]
        """
        return await User.from_username(self, username)

    async def get_user_from_id(self, account_id: str) -> Optional[User]:
        """
        Get a User object from an account ID.

        :param account_id: Account ID to look up.
        :type account_id: str
        :return: User object if found, None otherwise.
        :rtype: Optional[User]
        """
        return await User.from_id(self, account_id)

    def get_character_by_slug(self, slug: str) -> Optional[Character]:
        """
        Get a Character object by its slug.

        :param slug: Character slug.
        :type slug: str
        :return: Character object if found, None otherwise.
        :rtype: Optional[Character]
        """
        return self.character_manager.get_character_by_slug(slug)

    def get_character_from_key(self, key: str) -> Optional[Character]:
        """
        Get a Character object by its key.

        :param key: Character key.
        :type key: str
        :return: Character object if found, None otherwise.
        :rtype: Optional[Character]
        """
        return self.character_manager.get_character_by_key(key)

    def get_character_from_name(self, name: str) -> Optional[Character]:
        """
        Get a Character object by its name.

        :param name: Character name.
        :type name: str
        :return: Character object if found, None otherwise.
        :rtype: Optional[Character]
        """
        return self.character_manager.get_character_by_name(name)

    def get_map_from_key(self, key: str) -> Optional[str]:
        """
        Get a map name from its key.

        :param key: Map key.
        :type key: str
        :return: Map name if found, None otherwise.
        :rtype: Optional[str]
        """
        return self.maps.get(key)

    async def custom_request(self, endpoint: str) -> Dict[str, Any]:
        """
        Perform a custom GET request to a given endpoint on the MultiVersus API.

        :param endpoint: API endpoint to request.
        :type endpoint: str
        :return: JSON response from the API.
        :rtype: Dict[str, Any]
        """
        return await self.request(endpoint)


# Example usage
async def main():
    """
    Example usage of the MvsAPIWrapper class.
    """
    async with MvsAPIWrapper() as api:
        try:
            user = await User.from_username(api, "taetae")
            match = await user.get_most_recent_match()
            print("Map: " + match.map)
            print("Gamemode: " + match.mode)
            print("Winner: " + str(match.winning_team_index))
            print("Score: " + " - ".join(str(score) for score in match.score))
        except aiohttp.ClientError as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())