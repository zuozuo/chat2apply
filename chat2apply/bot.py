from __future__ import annotations
import json
import traceback

from typing import Any, Dict, List, Optional
from logging import Logger

from pydantic import Extra

from langchain.base_language import BaseLanguageModel
from langchain.callbacks.manager import (
    AsyncCallbackManagerForChainRun,
    CallbackManagerForChainRun,
    Callbacks,
)

from langchain.chains.base import Chain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain.schema import SystemMessage

from .user import User
from .prompts import SYSTEM_PROMPT
from .console import BotConsole
from .function import Function
from .chat_memory import ChatMemory
from .logger import get_logger
from .agent import BaseAgent


class Bot(Chain):
    """A custom chain, which serves as a chatbot to help user find and apply for jobs"""

    user: User = User()
    """current user to chat with the bot"""
    company_name: str
    """Company name for which this chatbot works for"""
    bot_name: str = "GeniusBot"
    """Name of the bot"""
    function: Function = Function()
    history: ChatMemory = ChatMemory()
    logger: Logger = get_logger('dev')
    agents: Dict[str, BaseAgent] = {}
    prompt: ChatPromptTemplate = SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            template="You are a chatbot",
            input_variables=[],
        )
    )
    """Prompt object to use."""
    llm: BaseLanguageModel = ChatOpenAI(temperature=1, model="gpt-4")
    output_key: str = "text"  #: :meta private:

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def console(self):
        return BotConsole(name=self.bot_name)

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

    @property
    def system_message(self):
        content = SYSTEM_PROMPT.format(
            bot_name=self.bot_name,
            company_name=self.company_name,
            user_profile=self.user.as_json(),
        )
        # logger.info(content)
        return SystemMessage(content=content)

    def add_agent(self, agent):
        self.agents[agent.name] = agent

    # pylint: disable=W0221
    def run(
        self,
        message,
        callbacks: Callbacks = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> str:
        self.history.add_user_message(message)
        return self(kwargs, callbacks=callbacks, tags=tags)

    def log_history(self):
        self.logger.info("log chat history: ")
        for msg in self.history.messages:
            self.logger.info(f"{msg.type}: {msg.content}")
        self.console.system_print("log chat history to log file successfully!")

    def run_interactively(self):
        self.console.print_welcome_message()
        first_question = "Do you want to find a job?"
        self.console.ai_print(first_question)
        self.history.add_ai_message(first_question)
        while True:
            try:
                user_input = self.console.get_user_input()
                if user_input in ["quit", "q"]:
                    break
                if user_input == "history" or user_input == "his":
                    self.log_history()
                    continue
                if user_input == "show_prompt" or user_input == "sp":
                    self.console.system_print(self.system_message.content)
                    continue
                response = self.run(user_input)
                self.logger.info(response)
                function_call = response.get("function_call", None)
                if function_call:
                    self.handle_function_call(function_call)
                else:
                    self.print_and_save(response["text"])
            except KeyboardInterrupt:
                break

    def handle_function_call(self, params):
        try:
            self.logger.info(f"function_call triggered with params: {params}")
            name, args = self.parse_function_call(params)
            self.validate_arguments(name, args)

            # TODO: update_job_preference(args)

            # call agent with arguments and return
            agent = self.agents[name]
            result = agent.run(args)
            agent.callback(result, self)
        except Exception:
            self.logger.warning(traceback.format_exc())

    def print_and_save(self, msg):
        self.console.ai_print(msg)
        self.history.add_ai_message(msg)

    def validate_arguments(self, name, args):
        agent = self.agents[name]
        if not agent:
            raise ValueError(f"invalid arguments: {name} {args}")

        invalid_args = self.find_invalid_argument(name, args)
        if invalid_args:
            args_desc = invalid_args["properties"]["description"]
            msg = f"Great, to apply the job you need to provide: {args_desc}"
            self.print_and_save(msg)
            raise ValueError(f"invalid arguments: {name} {args}")

    def find_invalid_argument(self, name, arguments):
        agent = self.agents[name]
        func_properties = agent.func_specs["parameters"]["properties"]
        for key in arguments:
            value = arguments[key]
            if self.is_argument_valid(value, func_properties[key]['type']):
                continue
            return {
                'name': key,
                'properties': func_properties[key]
            }
        return {}

    def safe_parse_arguments(self, args_str):
        try:
            return json.loads(args_str)
        except Exception as e:
            raise ValueError(f"invalid function_call arguments: {args_str}") from e

    def parse_function_call(self, params):
        name = params.get('name') or ''
        _args = params.get('arguments') or '{}'
        args = self.safe_parse_arguments(_args)
        if self.agents[name]:
            return name, args
        raise ValueError(f"invalid function: name={name} params={params}")

    def is_argument_valid(self, value, value_type):
        if value_type == 'string':
            return value != "" and value != 'any' and value is not None
        if value_type == 'integer':
            return value > 0
        if value_type == 'boolean':
            return True
        return False

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
        messages = [self.system_message] + self.history.messages
        response = self.llm.predict_messages(
            messages,
            callbacks=callbacks,
            functions=self.function.specs,
        )

        # If you want to log something about this run, you can do so by calling
        # methods on the `run_manager`, as shown below. This will trigger any
        # callbacks that are registered for that event.
        if run_manager:
            run_manager.on_text("Log something about this run")

        return {self.output_key: response.content, **response.additional_kwargs}

    async def _acall(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[AsyncCallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        pass

    @property
    def _chain_type(self) -> str:
        return "chat_to_apply"
