from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from prompts import SYSTEM_PROMPT

system_message_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        template=SYSTEM_PROMPT,
        input_variables=["company_name"],
    )
)
chat_prompt_template = ChatPromptTemplate.from_messages([system_message_prompt])
chat = ChatOpenAI(temperature=0.9)
chain = LLMChain(llm=chat, prompt=chat_prompt_template)
