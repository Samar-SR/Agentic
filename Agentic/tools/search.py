

# Search Information Tool
search_information = {
    "name": "search_information",
    "description": "In a single request generate the latest search results from internet.",
    "strict": True,
    "parameters": {
        "type": "object",
        "required": [
            "user_query"
        ],
        "properties": {
            "user_query": {
                "type": "string",
                "description": "This is the original and complete user query."
            },
        },
        "additionalProperties": False
    }
}


# Base tool to call in Gorq API
# This defines the structure of the tool that can be called by the Groq API.
tools = [
    {
        "type": "function",
        "function": search_information  # This refers to the dictionary defined above.
    }
]
