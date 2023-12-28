from typing import List

import yaml
from aiohttp import ClientSession
from dotenv import dotenv_values

from HomeManager import HomeManager

_env_ = dotenv_values('../.env')


class NeighborhoodManager:
    def __init__(self, session: ClientSession):
        self.homes: List = []
        self._load_local: bool = False
        # Initializing homes with keys and IDs from environment variables
        self.load_yaml_config(session)

    @staticmethod
    def count_homes():
        """
        Count the number of pairs of PUB_ and PRI_ keys stored within the .env file.

        Returns:
            int: The count of PUB_ and PRI_ pairs found.
        """
        count = 0
        n = 1  # Start with index 1 for PUB_1, PRI_1
        while True:
            pub_variable = f'PUB_{n}'
            pri_variable = f'PRI_{n}'

            # Check if both PUB_ and PRI_ variables exist in _env_
            if pub_variable in _env_ and pri_variable in _env_:
                count += 1
                n += 1
            else:
                break  # Exit the loop if either variable is not found

        return count

    def load_yaml_config(self, session: ClientSession):
        with open('../config.yaml', 'r') as file:
            yaml_content = yaml.safe_load(file)
        count = self.count_homes()
        self._load_local: bool = yaml_content.get('load_local', False)

        for home in range(1, count + 1):  # type: dict
            self.homes.append(HomeManager(session,
                                          key=_env_.get('PRI_' + str(home)),
                                          id=_env_.get('PUB_' + str(home)),
                                          unique_id=str(home)))

    async def build_neighborhood(self):
        # Initializing each home asynchronously
        for home in self.homes:  # type: HomeManager
            await home.init_home()

    async def load_data(self):
        # Loading data for each home asynchronously
        for home in self.homes:  # type: HomeManager
            await home.fetch_temperature_data(self._load_local)
            print('=' * 100)
