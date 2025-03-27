from groq import Groq
from tools.search import tools
from prompt.prompt import  gorq_prompt, gorq_summary
from settings import settings
from tools.tool_action import FUNCTION_MAPPING
from typing import List
from openai import OpenAI
import re


#Model Name
model = 'deepseek-r1-distill-llama-70b'

#Client for Groq API
client = Groq(api_key=settings.Gorq_API)

#Client for Summary API after tool output
summary_client = Groq(api_key=settings.Gorq_API)




class GroqAction():
    """
        This class handles interactions with the Groq API for processing user queries and utilizing tools.
    """

    def __init__(self,user_query:str):
        """
                Initializes the GroqAction with a user query.

                Args:
                    user_query (str): The user's query to be processed.
        """
        self.user_query = user_query

    async def __groq_api(self):

        """
                Sends a request to the Groq API to process the user query, potentially using tools.

                Returns:
                    ChatCompletion: The response from the Groq API.
        """

        result = client.chat.completions.create(
            model=model,
            messages=[
                        gorq_prompt,
                          {
                            "role" : "user",
                            "content" : f'Answer the user query { self.user_query }'
                           }
                    ],
            tools=tools,
            tool_choice="auto"
        )
        return result



    async def __groq_result_summaries(self,user_query: str, link_list : List) -> str:

        """
                Summarizes the results obtained from external links using the Groq API.

                Args:
                    user_query (str): The original user query.
                    link_list (List): A list of URLs to summarize.

                Returns:
                    str: The summarized content.
        """

        result = summary_client.chat.completions.create(
            model=model,
            messages=[
                gorq_summary,
                {
                    "role": "user",
                    "content": f" user question : { user_query } , links : { ' , '.join([ i for i in link_list ] ) } "
                }
            ],
        )

        data = result.choices[0].message.content

        return await  self.__data_cleaning(tag='think',data =data)



    async def __data_cleaning(self,tag: str,data : str) ->  str:

        """
        Cleans the data by removing specific tags and their content.

        Args:
            tag (str): The tag to remove (e.g., 'think').
            data (str): The data to clean.

        Returns:
            str: The cleaned data.
        """


        pattern = rf"<{tag}>.*?</{tag}>"
        data = re.sub(pattern, "", data, flags=re.DOTALL)

        return data



    async def __tool_result(self,tool_list : List) -> str:

        """
        Processes the results from the tools called by the Groq API.

        Args:
            tool_list (List): A list of tool call objects from the Groq API response.

        Returns:
            str: The summarized output from the tool results.
        """

        results = []
        for i in tool_list:
            # Retrieve the class associated with the tool name from the FUNCTION_MAPPING
            cls = FUNCTION_MAPPING[i.function.name]
            # Process the user query using the tool's process method
            output = await cls.process(self.user_query)
            # Extend the results list with the output from the tool
            results.extend([i for i in output])

        # Summarize the results using the Groq API
        output = await self.__groq_result_summaries(self.user_query,results)
        return output




    async def gorq_process(self) -> str:
        """
        The main method for processing the user query using the Groq API and tools.

        Returns:
            str: The final output, either from the Groq API directly or from tool processing.
        """

        result = await self.__groq_api()
        # Check if the Groq API response includes tool calls
        if result.choices[0].message.tool_calls:
            # Process the tool calls and get the summarized output
            output = await self.__tool_result(result.choices[0].message.tool_calls)
        else:
            # If no tool calls, use the content directly from the Groq API response
            output = result.choices[0].message.content

        return output




















