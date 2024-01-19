from langchain.llms import OpenAI
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
import argparse
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


"""Add flag arguments to your function like this"""
parser = argparse.ArgumentParser()
parser.add_argument("--task", default="create function that returns number from 1-10")
parser.add_argument("--language", default="python")
args = parser.parse_args()
llm = OpenAI(
    openai_api_key=os.environ['API_KEY']  # OpenAi Api key
)

code_prompt = PromptTemplate(
    template="Write a very short {language} function that will {task}",
    input_variables=["language", "task"])


send_code_prompt = PromptTemplate(
    input_variables=["language", "code"],
    template="Write a test for following {language} code: \n {code}"
)
code_chain = LLMChain(
    llm=llm,
    prompt=code_prompt,
    output_key="code"
)

test_chain = LLMChain(
    llm=llm,
    prompt=send_code_prompt,
    output_key="test"
)

chain = SequentialChain(
    chains=[code_chain, test_chain],
    input_variables=["task", "language"],
    output_variables=["test", "code"]
)
result = chain({
    "language": args.language,
    "task": args.task
})

print("code______________________________________")
print(result["code"])
print("test______________________________________")
print(result["test"])
