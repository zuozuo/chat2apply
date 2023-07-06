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
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage, AIMessage

from .user import User
from .prompts import SYSTEM_PROMPT
from .functions import Functions

class Bot(Chain):
    """A custom chain, which serves as a chatbot to help user find and apply for jobs"""

    """current user to chat with the bot"""
    user: User = User()

    """Company name for which this chatbot works for"""
    company_name: str

    """Functions"""
    functions: Functions = Functions()

    """Prompt object to use."""
    prompt: ChatPromptTemplate = SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            template=SYSTEM_PROMPT,
            input_variables=["company_name"],
        )
    )

    llm: BaseLanguageModel = ChatOpenAI(temperature=0.9)
    output_key: str = "text"  #: :meta private:

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
        kwargs['message'] = message
        _output_key = self._run_output_key
        return self(kwargs, callbacks=callbacks, tags=tags, metadata=metadata)[
            _output_key
        ]

    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        message = inputs.pop('message', '')
        messages = [
            self.prompt.format(**inputs),
            HumanMessage(content=message),
        ]
        # Whenever you call a language model, or another chain, you should pass
        # a callback manager to it. This allows the inner run to be tracked by
        # any callbacks that are registered on the outer run.
        # You can always obtain a callback manager for this by calling
        # `run_manager.get_child()` as shown below.
        callbacks = run_manager.get_child() if run_manager else None
        response = self.llm.predict_messages(
            messages,
            callbacks=callbacks,
            functions=self.functions.function_specs
        )

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
