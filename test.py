import sys

from chat2apply.bot import Bot

bot = Bot(company_name='KFC')

# bot.run("Answer briefly. What are the first 3 colors of a rainbow?")
# bot.run("and the next 4")
#

message = " ".join(sys.argv[1:])
print(message)
response = bot.run(message)
print(response)
