from chat2apply import Bot, User, ApplyJobAgent, SearchJobAgent

user = User(name="zorro1", phone="18601257149", email="zuo@gmail.com")

bot = Bot(user=user, bot_name="GeniusBot", company_name="company_name")
bot.add_agent(ApplyJobAgent())
bot.add_agent(SearchJobAgent())

print(bot.agents)
# bot.run_interactively()

# message = " ".join(sys.argv[1:])
# print(message)
# response = bot.run(message)
# print(response)
