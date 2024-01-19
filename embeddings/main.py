import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI


load_dotenv()

api_key = os.environ['API_KEY']

# Add you api key here
chat = ChatOpenAI(
    openai_api_key=api_key,
    verbose=True
)

