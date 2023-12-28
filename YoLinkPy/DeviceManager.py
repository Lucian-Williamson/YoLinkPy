import json
from typing import Any, Type

from yolink.const import ATTR_DEVICE_TH_SENSOR, ATTR_DEVICE_ID, ATTR_DEVICE_NAME, ATTR_DEVICE_TOKEN, ATTR_DEVICE_TYPE, \
    ATTR_DEVICE_PARENT_ID, ATTR_DEVICE_MOTION_SENSOR, ATTR_DEVICE_LEAK_SENSOR
from yolink.device import YoLinkDeviceMode, YoLinkDevice
from yolink.home_manager import YoLinkHome

from AuthManager import AuthManager
from MsgManager import MsgListener

CELSIUS_TO_FAHRENHEIT_MULTIPLIER = 9 / 5
CELSIUS_TO_FAHRENHEIT_OFFSET = 32


class YoLinkDeviceModeAdapter(Type):
    @classmethod
    def validate_python(cls, obj: Any) -> Any:
        return YoLinkDeviceMode(**obj)


class DeviceManager:
    """
    Manages devices by loading, storing, and fetching data.
    """

    def __init__(self):

        self._data = {}  # Initialize an empty dictionary to store device data

    @staticmethod
    def invert(attr: str) -> str:
        """
        Converts internal attribute names to external ones.
        """
        attribute_mapping = {
            'device_id'       : ATTR_DEVICE_ID,
            'device_name'     : ATTR_DEVICE_NAME,
            'device_token'    : ATTR_DEVICE_TOKEN,
            'device_type'     : ATTR_DEVICE_TYPE,
            'device_parent_id': ATTR_DEVICE_PARENT_ID,
        }
        return attribute_mapping.get(attr)

    @staticmethod
    def load_data(public_id) -> dict:
        """
        Loads device data from a JSON file.
        """
        try:
            with open(f'../data/{public_id}.json', 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def store_data(self, data: dict, id: str) -> None:
        """
        Stores device data as JSON.
        """
        with open(f'../data/{id}.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        self._data = data

    async def fetch_temperature_data(self, yo_link_home: YoLinkHome) -> None:
        """
        Fetches temperature data for YoLink devices and prints it.
        """
        for device_data in self._data.values():
            device_type = device_data[ATTR_DEVICE_TYPE]

            device_instance = YoLinkDeviceModeAdapter.validate_python(device_data)
            device = YoLinkDevice(device=device_instance, client=yo_link_home._http_client)
            state = await device.fetch_state()

            if device_type in [ATTR_DEVICE_MOTION_SENSOR, ATTR_DEVICE_LEAK_SENSOR]:
                temperature_celsius = state.data['state']['devTemperature']
            elif device_type == ATTR_DEVICE_TH_SENSOR:
                temperature_celsius = state.data['state']['temperature']
            else:
                continue  # Skip unknown device types

            temperature_fahrenheit = round(
                temperature_celsius * CELSIUS_TO_FAHRENHEIT_MULTIPLIER + CELSIUS_TO_FAHRENHEIT_OFFSET, 2
            )

            print(f"{device_data[ATTR_DEVICE_NAME]:<30} \t {device_type:<15} \t {temperature_fahrenheit}")

    @staticmethod
    def _extract_device_data(home_devices: dict) -> dict:
        """
        Extracts and formats device data from home devices.
        """
        device_data = {}
        for device_id, device in home_devices.items():
            device_dict = DeviceManager._format_device_info(device)
            device_data[device_id] = device_dict  # Store formatted device information
        return device_data

    @staticmethod
    def _format_device_info(device: YoLinkDevice) -> dict:
        """
        Formats device information for storage.
        """
        device_dict = {
            DeviceManager.invert(key): value for key, value in device.__dict__.items() if not key.startswith('_')
        }
        device_dict.pop(None, None)  # Remove 'None' key if present
        device_dict[ATTR_DEVICE_PARENT_ID] = None  # Set ATTR_DEVICE_PARENT_ID to None if not present
        return device_dict

    async def setup(self, yo_link_home: YoLinkHome, auth_manager: AuthManager, msg_manager: MsgListener) -> None:
        await yo_link_home.async_setup(auth_manager, msg_manager)

    def _build_temperature_device_dict_(self, yo_link_home: YoLinkHome) -> dict:
        """
        Extracts and organizes device data related to temperature monitoring from a YoLinkHome instance.

        Args:
        - yo_link_home (YoLinkHome): Instance of YoLinkHome containing device information.

        Returns:
        - dict: A dictionary containing device data for devices associated with temperature monitoring.
        """
        all_device_data = DeviceManager._extract_device_data(yo_link_home._home_devices)
        temperature_devices = {}
        for device_data in all_device_data.values():
            if device_data[ATTR_DEVICE_TYPE] in [ATTR_DEVICE_MOTION_SENSOR, ATTR_DEVICE_LEAK_SENSOR,
                                                 ATTR_DEVICE_TH_SENSOR]:
                temperature_devices[device_data['deviceId']] = device_data
        return temperature_devices

    async def load_devices(self, yo_link_home: YoLinkHome, unique_id: str, _load_local: bool) -> None:
        """
        Loads devices and their details from YoLinkHome.
        """
        if self._data:
            return  # Return if data is already populated

        _devices = {}
        if _load_local:
            # Attempt to pull local data from json files...
            try:
                _devices = self.load_data(public_id=unique_id)
            except FileNotFoundError:
                pass

        if not _devices:
            _devices = self._build_temperature_device_dict_(yo_link_home)

        self.store_data(data=_devices, id=unique_id)  # Store the device information as JSON
