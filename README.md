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
bot = Bot(company_name='KFC')
bot.run_interactively()
```

## run test
```shell
pytest -s
```
