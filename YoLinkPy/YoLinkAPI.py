import asyncio
from aiohttp import ClientSession
from NBHManager import NeighborhoodManager  # Importing necessary modules/classes


async def main():
    # Establishing an asynchronous HTTP session
    async with ClientSession() as session:
        # Initializing NeighborhoodManager instance for neighborhood management
        nbh_mgr = NeighborhoodManager(session)
        try:
            # Building the neighborhood data asynchronously
            await nbh_mgr.build_neighborhood()
            # Loading additional data asynchronously
            await nbh_mgr.load_data()
        except Exception as e:
            # Handling any exceptions that occur during the process
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Running the main function within an event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
