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

## run test
```shell
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
