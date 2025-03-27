from log import logging
from services.gorq import GroqAction


# Base Action to process user query
class DataPipeline:

    def __init__(self, user_query: str):
        self.user_query = user_query

    async def process(self) -> dict:
        # Service to process user query
        logging.info('Calling Gorq Action')
        result = GroqAction(self.user_query)
        output = await result.gorq_process()

        return output
