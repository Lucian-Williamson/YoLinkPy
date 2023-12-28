from dotenv import dotenv_values
from yolink.home_manager import YoLinkHome

from AuthManager import AuthManager
from aiohttp import ClientSession
from DeviceManager import DeviceManager
from MsgManager import MsgListener

_env_ = dotenv_values('../.env')


class HomeManager:
    """
    Manages the initialization and data retrieval from YoLinkHome devices.

    Attributes:
        auth_mgr (AuthManager): Manages authentication for accessing YoLinkHome.
        message_listener (MsgListener): Listens to messages from YoLinkHome devices.
        yolink_home (YoLinkHome): Represents the YoLinkHome instance.
        device_mgr (DeviceManager): Manages devices connected to YoLinkHome.
        public_id: Unique ID for this home manager

    Methods:
        async def init_home(self):
            Initializes the YoLinkHome and sets up connected devices for interaction.

        async def fetch_temperature_data(self):
            Loads devices and fetches temperature data asynchronously from YoLinkHome devices,
            handling any setup failures
    """

    def __init__(self, session: ClientSession, key: str, id: str , unique_id: str):
        assert isinstance(key, str) and isinstance(id, str) and isinstance(unique_id, str)
        self.auth_mgr: AuthManager = AuthManager(session, key=key, id=id)
        self.message_listener: MsgListener = MsgListener()
        self.yolink_home: YoLinkHome = YoLinkHome()
        self.device_mgr: DeviceManager = DeviceManager()
        self._uid: str = unique_id

    async def init_home(self):
        await self.device_mgr.setup(self.yolink_home, self.auth_mgr, self.message_listener)

    async def fetch_temperature_data(self, _load_local: bool = False):
        try:
            await self.device_mgr.load_devices(self.yolink_home, unique_id=self._uid, _load_local = _load_local)
            await self.device_mgr.fetch_temperature_data(self.yolink_home)
        except Exception as e:
            # Handle setup failure
            print(f"Setup failed: {e}")
