from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import Extra

from langchain.base_language import BaseLanguageModel
from langchain.callbacks.manager import (
    AsyncCallbackManagerForChainRun,
    CallbackManagerForChainRun,
)
from langchain.chains.base import Chain
from langchain.prompts.base import BasePromptTemplate
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage, AIMessage

from .user import User
from .prompts import SYSTEM_PROMPT
from .functions import Functions
from .chat_memory import ChatMemory
from .console import BotConsole

class Bot(Chain):
    """A custom chain, which serves as a chatbot to help user find and apply for jobs"""

    user: User = User()
    """current user to chat with the bot"""

    company_name: str
    """Company name for which this chatbot works for"""

    bot_name: str = 'Mia'
    """Name of the bot"""

    functions: Functions = Functions()
    """Functions"""

    memory: ChatMemory = ChatMemory()

    prompt: ChatPromptTemplate = SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            template=SYSTEM_PROMPT,
            input_variables=["company_name", "history", "input"],
        )
    )
    """Prompt object to use."""

    # console: BotConsole = BotConsole()
    llm: BaseLanguageModel = ChatOpenAI(temperature=0.9, model='gpt-4')
    output_key: str = "text"  #: :meta private:

    @property
    def console(self):
        return BotConsole(name=self.bot_name)

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def input_keys(self) -> List[str]:
        """Will be whatever keys the prompt expects.

        :meta private:
        """
        return self.prompt.input_variables

    @property
    def output_keys(self) -> List[str]:
        """Will always return text key.

        :meta private:
        """
        return [self.output_key]

    def run(
        self,
        message,
        company_name=None,
        callbacks: Callbacks = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> str:
        kwargs['company_name'] = company_name or self.company_name
        kwargs['input'] = message
        return self(kwargs, callbacks=callbacks, tags=tags, metadata=metadata)

    def run_interactively(self):
        self.console.print_welcome_message()
        # messages.append({"role": "user", "content": 'Do you want to find a job?'})
        while True:
            try:
                user_input = self.console.get_user_input()

                if user_input in ['quit', '\q', 'q']:
                    break
                if user_input == 'show_messages':
                    print_json('show_messages')
                    continue

                response = self.run(user_input)
                print(response)
                self.console.ai_print(response['text'])
                # function_call = assistant_message.get('function_call', None)
                # if function_call:
                #     handle_function_call(function_call)
                # else:
                #     mia_print(assistant_message['content'])
            except KeyboardInterrupt:
                break

    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        # Whenever you call a language model, or another chain, you should pass
        # a callback manager to it. This allows the inner run to be tracked by
        # any callbacks that are registered on the outer run.
        # You can always obtain a callback manager for this by calling
        # `run_manager.get_child()` as shown below.
        callbacks = run_manager.get_child() if run_manager else None
        response = self.llm.predict_messages(
            [self.prompt.format(**inputs)],
            callbacks=callbacks,
            functions=self.functions.function_specs,
        )
        print(response)
        # function_call={"name": "recommend_jobs"}

        # If you want to log something about this run, you can do so by calling
        # methods on the `run_manager`, as shown below. This will trigger any
        # callbacks that are registered for that event.
        if run_manager:
            run_manager.on_text("Log something about this run")

        return {self.output_key: response.content}

    async def _acall(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[AsyncCallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        pass

    @property
    def _chain_type(self) -> str:
        return "chat_to_apply"
