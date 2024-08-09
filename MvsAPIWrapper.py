import string
import requests
import os
from dotenv import load_dotenv


class MvsAPIWrapper:
    def __init__(self, steamToken=None):
        self.url = "https://dokken-api.wbagora.com/"
        self.session = requests.Session()

        if steamToken is None:
            load_dotenv()  # Load environment variables from .env file
            steamToken = os.getenv('MULTIVERSUS_TOKEN')

        self.refresh_token(steamToken)

    def refresh_token(self, steamToken: string = None):
        if steamToken is not None:
            self.steamToken = steamToken

        tempHeaders = {
            'x-hydra-api-key': '51586fdcbd214feb84b0e475b130fce0',
            'x-hydra-user-agent': 'Hydra-Cpp/1.132.0',
            'Content-Type': 'application/json',
            'x-hydra-client-id': '47201f31-a35f-498a-ae5b-e9915ecb411e'
        }
        tempBody = {"auth": {"fail_on_missing": 1, "steam": self.steamToken}, "options": ["wb_network"]}
        req = self.session.post(f"{self.url}access", json=tempBody, headers=tempHeaders).json()
        self.token = req["token"]
        self.header = {
            'x-hydra-api-key': '51586fdcbd214feb84b0e475b130fce0',
            'x-hydra-user-agent': 'Hydra-Cpp/1.132.0',
            'Content-Type': 'application/json',
            'x-hydra-access-token': self.token
        }

    def get_player_profile(self, account_id):
        """
        Get the profile of a player using their account ID.
        """
        endpoint = f"{self.url}profiles/{account_id}"
        response = self.session.get(endpoint, headers=self.header)
        response.raise_for_status()
        return response.json()


# Example usage
if __name__ == "__main__":
    api = MvsAPIWrapper()

    try:
        player_profile = api.get_player_profile('62873f49d78c32e26df3a47c')
        print("Player Profile:", player_profile)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")