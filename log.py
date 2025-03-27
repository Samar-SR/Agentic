import logging

# Configure logging globally
logging.basicConfig()

# Create a named logger
logger = logging.getLogger("Agent")
logger.setLevel(logging.DEBUG)  # Ensure it captures all logs
