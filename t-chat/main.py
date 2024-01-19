import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory, ConversationSummaryMemory

load_dotenv()

api_key = os.environ['API_KEY']

# Add you api key here
chat = ChatOpenAI(
    openai_api_key=api_key,
    verbose=True
)

"""If you want ot store question ask by you and the AI generated answer you can use this one
(will be saved in same directory next to main file for future use)"""
# memory = ConversationSummaryMemory(
#     memory_key="messages", return_messages=True,
#     chat_memory=FileChatMessageHistory("messages.json")
# )

memory = ConversationSummaryMemory(
    memory_key="messages", return_messages=True,
    llm=chat
)

prompt = ChatPromptTemplate(
    input_variables=["content", "messages"],
    messages=[MessagesPlaceholder(variable_name="messages"),
              HumanMessagePromptTemplate.from_template("{content}")]
)

chain = LLMChain(
    llm=chat,
    prompt=prompt,
    memory=memory,
    verbose=True
)

while True:
    content = input("Ask your question here======> ")
    print(f"You entered : {content}")
    if not content:
        content = "what you can do 10 bullet points"
    result = chain({
        "content": content
    })
    print(result['text'])
