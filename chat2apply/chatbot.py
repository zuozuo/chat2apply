from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from .functions import Functions
from .prompts import SYSTEM_PROMPT

class Chatbot:
    """A chatbot to help user find and apply for jobs"""

    def __init__(self, company_name):
        self.company_name = company_name
        self.model = self.init_model(company_name=company_name)
        self.functions = Functions(model=self.model)

    def init_model(self, company_name=None):
        _company_name = company_name or self.company_name
        if not _company_name:
            raise 'company_name should not be blank'

        system_message_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=SYSTEM_PROMPT,
                input_variables=["company_name"],
            )
        )
        prompt = SystemMessage(content=)
        chat = ChatOpenAI(temperature=0.9)
        llm_kwargs = {
            'functions': Functions.function_specs
        }
        return LLMChain(
            llm=chat,
            prompt=prompt,
            llm_kwargs=llm_kwargs,
        )

    def chat(self, user_message):
        inputs = {
            'company_name': self.company_name
        }
        self.model.run(inputs, )
