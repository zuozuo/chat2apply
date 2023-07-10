import sys
from chat2apply.bot import Bot

bot = Bot(bot_name="GeniusBot", company_name="company_name")
bot.run_interactively()

message = " ".join(sys.argv[1:])
print(message)
response = bot.run(message)
print(response)
