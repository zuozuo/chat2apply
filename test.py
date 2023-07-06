import sys

from chat2apply.bot import Bot

bot = Bot(company_name='KFC')
bot.run_interactively()

# message = " ".join(sys.argv[1:])
# print(message)
# response = bot.run(message)
# print(response)
