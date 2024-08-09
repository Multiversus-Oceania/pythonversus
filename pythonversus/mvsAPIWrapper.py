import string
import requests
import os
from dotenv import load_dotenv


class MvsAPIWrapper:
    def __init__(self, steam_token=None):
        self.header = None
        self.token = None
        self.steam_token = None
        self.url = "https://dokken-api.wbagora.com/"
        self.session = requests.Session()

        if steam_token is None:
            load_dotenv()  # Load environment variables from .env file
            steam_token = os.getenv('MULTIVERSUS_TOKEN')

        self.refresh_token(steam_token)

    def refresh_token(self, api_token: string = None):
        if api_token is not None:
            self.steam_token = api_token

        temp_headers = {
            'x-hydra-api-key': '51586fdcbd214feb84b0e475b130fce0',
            'x-hydra-user-agent': 'Hydra-Cpp/1.132.0',
            'Content-Type': 'application/json',
            'x-hydra-client-id': '47201f31-a35f-498a-ae5b-e9915ecb411e'
        }
        temp_body = {"auth": {"fail_on_missing": 1, "steam": self.steam_token}, "options": ["wb_network"]}
        req = self.session.post(f"{self.url}access", json=temp_body, headers=temp_headers).json()
        self.token = req["token"]
        self.header = {
            'x-hydra-api-key': '51586fdcbd214feb84b0e475b130fce0',
            'x-hydra-user-agent': 'Hydra-Cpp/1.132.0',
            'Content-Type': 'application/json',
            'x-hydra-access-token': self.token
        }

    def api_request(self, endpoint):
        response = self.session.get(endpoint, headers=self.header)
        response.raise_for_status()
        return response.json()

    def get_player_profile(self, account_id):
        """
        Get the profile of a player using their account ID.
        """
        endpoint = f"{self.url}profiles/{account_id}"
        return self.api_request(endpoint)

    def get_player_account(self, account_id):
        """
        Get the account of a player using their account ID.
        """
        endpoint = f"{self.url}accounts/{account_id}"
        return self.api_request(endpoint)

    def get_id_from_username(self, account_name, limit=5):
        endpoint = f"{self.url}profiles/search_queries/get-by-username/run?username={account_name}&limit={limit}"
        players = self.api_request(endpoint)

        # Check if the username matches
        # If the search length = 1 then we have probably found the correct player
        search_length = len(players["results"])

        if search_length == 1:
            return players["results"][0]["result"]["account_id"]
        else:
            for player in players["results"]:
                account_id = player["result"]["account_id"]
                account_data = self.get_player_account(account_id)
                username = account_data["identity"]["alternate"]["wb_network"][0]["username"]
                if username and username.lower() == account_name.lower():
                    return account_id

        return "Failed to find matching account"


# Example usage
if __name__ == "__main__":
    api = MvsAPIWrapper()

    try:
        # player_profile = api.get_player_profile('62873f49d78c32e26df3a47c')
        player_name = "taetae"
        # print("Player Profile:", player_profile)
        print("Searching for account with username {}".format(player_name))
        print("Player search: ", api.get_id_from_username(player_name))
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
