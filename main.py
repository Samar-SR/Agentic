from fastapi import FastAPI
from action.base_action import DataPipeline
from log import logger

app = FastAPI()


@app.post('/result')
async def results(query: str):
    """
    API endpoint to process a user query and return the result.

    Args:
        query (str): The user's query.

    Returns:
        str: The result of processing the query.
    """
    logger.info('Search Started')
    base = DataPipeline(query)
    result = await base.process()

    return result
