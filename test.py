import sys
from chat2apply import Bot, User

user1 = User(name="zorro", phone="18601257149", email="zuo@gmail.com")
user2 = User(name="zuo", email="zuo@gmail.com")
user3 = User(name="zuo", phone="18601257149")

bot = Bot(user=user2, bot_name="GeniusBot", company_name="company_name")
bot.run_interactively()

# message = " ".join(sys.argv[1:])
# print(message)
# response = bot.run(message)
# print(response)
