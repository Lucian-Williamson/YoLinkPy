from time import time

import requests
from aiohttp import ClientSession
from dotenv import dotenv_values
from yolink.auth_mgr import YoLinkAuthMgr

_env_ = dotenv_values('../.env')


class AuthManager(YoLinkAuthMgr):
    """Custom YoLink API Authentication Manager."""

    def __init__(self, session: ClientSession):
        """Custom YoLink Auth Manager"""
        super().__init__(session)
        self.UAID: str = ''
        self.SecretKey: str = ''
        self.SVR_URL: str = ''
        self.API_URL: str = ''
        self._token_expiration: int = 0
        self._time_since: int = 0
        self._tolken: str = ''
        self._load_env_()

    def _load_env_(self):
        config_vars = ['UAID', 'SecretKey', 'SVR_URL', 'API_URL']
        for var in config_vars:
            setattr(self, var, _env_.get(var))
            if getattr(self, var) is None:
                raise NotImplementedError

    def _use_active_token(self):
        if time() - self._time_since < self._token_expiration:
            return self._tolken
        else:
            print("Refreshing Token")
            return self.generate_access_token()

    def access_token(self) -> str:
        """Get auth token."""
        return self._use_active_token()

    async def check_and_refresh_token(self) -> str:
        """Check and refresh token."""
        return self._use_active_token()

    def generate_access_token(self) -> str:
        """Generate access token."""
        payload = {
            "grant_type"   : "client_credentials",
            "client_id"    : self.UAID,
            "client_secret": self.SecretKey
        }
        response = requests.post(f"{self.SVR_URL}/open/yolink/token", data=payload)
        print(f"Request {'successful' if response.status_code == 200 else 'failed'}. Code {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            self._tolken = data.get('access_token')
            self._token_expiration = data.get('expires_in')
            self._time_since = time()
            return self._tolken
        else:
            print(f"Request failed with status code {response.status_code} \n {response.text}")
            return ''
