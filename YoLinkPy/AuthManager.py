from time import time

import requests
from aiohttp import ClientSession
from yolink.auth_mgr import YoLinkAuthMgr


class AuthManager(YoLinkAuthMgr):
    """Custom YoLink API Authentication Manager."""

    def __init__(self, session: ClientSession, id: str, key: str):
        """
        Initializes the Custom YoLink Authentication Manager.

        Args:
        - session (ClientSession): Aiohttp ClientSession for handling HTTP requests.
        - id (str): User account ID.
        - key (str): User account Secret Key.
        - public_id (str): Public identifier for the user.

        Attributes:
        - _UAID_ (str): User account ID.
        - _SecretKey_ (str): User account Secret Key.
        - _SVR_URL_ (str): YoSmart API server URL.
        - _API_URL_ (str): YoSmart API base URL.
        - _token_expiration_ (int): Token expiration time in seconds.
        - _time_since (int): Time since the last token update.
        - _token_ (str): Current access token.
        """
        super().__init__(session)
        self._UAID_: str = id
        self._SecretKey_: str = key
        self._SVR_URL_: str = "https://api.yosmart.com/"
        self._API_URL_: str = "https://api.yosmart.com/open/yolink/v2/api"
        self._token_expiration_: int = 0
        self._time_since: int = 0
        self._token_: str = ""

    def _use_active_token(self):
        """
        Checks and returns the active token if valid; otherwise, generates a new token.

        Returns:
        - str: Active access token.
        """
        if time() - self._time_since < self._token_expiration_:
            return self._token_
        else:
            print("Refreshing Token")
            return self.generate_access_token()

    def access_token(self) -> str:
        """
        Retrieves the current access token.

        Returns:
        - str: Current access token.
        """
        return self._use_active_token()

    async def check_and_refresh_token(self) -> str:
        """
        Checks and refreshes the access token.

        Returns:
        - str: Refreshed access token.
        """
        return self._use_active_token()

    def generate_access_token(self) -> str:
        """
        Generates a new access token.

        Returns:
        - str: Newly generated access token.
        """
        payload = {
            "grant_type": "client_credentials",
            "client_id": self._UAID_,
            "client_secret": self._SecretKey_,
        }
        response = requests.post(f"{self._SVR_URL_}/open/yolink/token", data=payload)
        print(
            f"Request {'successful' if response.status_code == 200 else 'failed'}. Code {response.status_code}"
        )
        if response.status_code == 200:
            data = response.json()
            self._token_ = data.get("access_token")
            self._token_expiration_ = data.get("expires_in")
            self._time_since = time()
            return self._token_
        else:
            print(
                f"Request failed with status code {response.status_code} \n {response.text}"
            )
            return ""
