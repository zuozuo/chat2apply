import sys

from chat2apply.bot import Bot
bot = Bot(company_name='company_name', bot_name='GeniusBot')
bot.run_interactively()

# message = " ".join(sys.argv[1:])
# print(message)
# response = bot.run(message)
# print(response)
