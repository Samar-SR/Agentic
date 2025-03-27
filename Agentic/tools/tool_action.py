from abc import abstractmethod, ABC
import requests
from config import url, headers

FUNCTION_MAPPING = {}  # Dictionary to store the mapping of tool names to their classes.


def action_register(cls):
    """
    Decorator to register a tool class in the FUNCTION_MAPPING.

    Args:
        cls: The tool class to register.

    Returns:
        The tool class.
    """
    FUNCTION_MAPPING[cls.name()] = cls()
    return cls


@action_register
class BaseAction(ABC):
    """
    Abstract base class for all tool actions.
    """

    @staticmethod
    def name():
        """
        Abstract method to get the name of the tool.

        Returns:
            None: Must be implemented by subclasses.
        """
        return None


@action_register
class PriceAction(BaseAction):
    """
    Tool action to search information.
    """

    @staticmethod
    def name():
        """
        Returns the name of the tool.

        Returns:
            str: The name of the tool ("search_information").
        """
        return "search_information"

    async def process(self, user_query: str):
        """
        Processes the user query by searching for information.

        Args:
            user_query (str): The user's query.

        Returns:
            list: A list of links related to the query.
            dict: If an exception occurs, returns a dictionary with the exception.
        """

        querystring = {"query": user_query, "limit": "2", "related_keywords": "false"}
        try:
            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()

            if data['results']:
                result = data['results'][0]

                links_of_result = [i['url'] for i in data['results']]

                return links_of_result
        except Exception as e:
            return {'exception': e}