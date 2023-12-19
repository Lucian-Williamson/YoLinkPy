import asyncio

from aiohttp import ClientSession
from yolink.home_manager import YoLinkHome

from AuthManager import AuthManager
from DeviceManager import DeviceManager
from MsgManager import MsgListener


async def main():
    # Create a session for HTTP requests
    async with ClientSession() as session:
        # Initialize custom authentication manager and message listener
        auth_mgr = AuthManager(session)
        message_listener = MsgListener()
        yh = YoLinkHome()

        device_mgr = DeviceManager()

        try:
            await device_mgr.load_devices(yh, auth_mgr, message_listener)
            await device_mgr.fetch_temperature_data(yh, auth_mgr, message_listener)
        except Exception as e:
            # Handle setup failure
            print(f"Setup failed: {e}")
        finally:
            # Close the session after execution
            await session.close()


if __name__ == "__main__":
    # Run the main function within an event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
