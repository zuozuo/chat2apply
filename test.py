import sys

from chat2apply.bot import Bot
bot = Bot(company_name='company_name', bot_name='GeniusBot')
bot.run_interactively()
# import ipdb; ipdb.set_trace(context=5)

# message = " ".join(sys.argv[1:])
# print(message)
# response = bot.run(message)
# print(response)
