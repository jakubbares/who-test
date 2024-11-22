from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from typing import List
import os
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field, validator
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from langchain_community.callbacks.infino_callback import get_num_tokens
from langchain_openai import ChatOpenAI, AzureOpenAI, AzureChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()


openai_key = os.getenv("AZURE_OPENAI_KEY")
openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")

print(openai_key, openai_api_version)

class Summary(BaseModel):
    summary: str = Field(description="Summary of the speech")

class Summarizer:
    model = AzureChatOpenAI(deployment_name="gpt-4o-mini", api_key=openai_key, api_version=openai_api_version)
    parser = PydanticOutputParser(pydantic_object=Summary)
    prompt = PromptTemplate(
        template="""You are supposed to return a summary with bullet points of the key points made during the speech
                Focus on actual propositions, agreements, factual claims, etc.
                \n{format_instructions}\n{transcript}\n""",
        input_variables=["transcript"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | model | parser
    def invoke(self, transcript):
        return self.chain.invoke({"transcript": transcript})
    
Summarizer().invoke(transcript=text)    


