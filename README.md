# chat2apply
An AI chatbot to help user find and apply jobs

## Run locally
clone the repository to local and run:
```
pip install -e .
```
then run code below:

```python
from chat2apply.bot import Bot
bot = Bot(company_name='KFC', bot_name='GeniusBot')
bot.run_interactively()
```
or you can view the code example in `test.py`

## How to debug the bot
when running locally with `bot.run_interactively` you can see the
conversation history on the interactive command line console with 
the debug log and error messages.
You can disable the debug log and error messages by setting logger to
`production_logger`:
```python
from chat2apply.bot import get_logger
logger = get_logger('production')
bot = Bot(company_name='KFC', bot_name='GeniusBot', logger=logger)
bot.run('hello')
# or 
# this is only used for debugging locally
bot.run_interactively()
```
then all the debug log and error messages will be printed to a log file
at: `/tmp/chatbot.log`, use the following command to check the log.

```shell
tail -f /tmp/chatbot.log
```

## run test
```shell
# this is not really working now
pytest -s
```

## How to save conservation history to database
subclass `ChatMemory` which is defined in `chat2apply/chat_memory.py`
```python
# a simple code example
from chat2apply.chat_memory import ChatMemory

class MysqlMemory(ChatMemory):
    def add_message(self, message):
        self.messages.append(message)
        # save the message to database here

    def clear(self):
        self.messages.clear()
        # delete message records here

    def load_history_messages(self):
        pass
        # load conservation history from database here
```

## How to implement a cunstom agent and add it to bot

1. subclass `BaseAgent` which is defined in `chat2apply/agent/base.py`
```python
# this is a simple code example to implement a cunstom agent
from .base import BaseAgent

class MyCustomAgent(BaseAgent):
    # for more infomation about function_specs please refer to the documentation:
    # https://platform.openai.com/docs/api-reference/chat/create#chat/create-functions
    @property
    def function_specs(self):
        return {
            "name": "my_custom",
            "description": "this is a custom agent",
            "parameters": {
                "type": "object",
                "properties": {
                    "property1": {
                        "type": "string",
                        "description": "property1 description","
                    },
                    "property2": {
                        "type": "string",
                        "description": "property2 description","
                    },
                },
                "required": ["property1"]
            },
        }

    # put the business logic here
    # args: { 'property1':'value1', 'property2':'value2'' }
    def run(self, args):
        return args

    # this function only used in the interactively mode for debugging purposes
    def callback(self, job, bot):
        pass
```

2. init a bot instance and add your custom agent to the bot's agent list
```python
from chat2apply import Bot, User, ApplyJobAgent, SearchJobAgent, MyCustomAgent

user = User(name="name", phone="phone number", email="email address")

bot = Bot(user=user, bot_name="GeniusBot", company_name="company_name")
bot.add_agent(ApplyJobAgent())
bot.add_agent(SearchJobAgent())
bot.add_agent(MyCustomAgent)
bot.run('hello')
```
