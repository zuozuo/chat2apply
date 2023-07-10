import sys
from chat2apply.bot import Bot

messages = [
    "I want to find a job",
    "Chicago",
    "Waiter",
    "full-time",
    "I am legally eligible to work in the USA",
]


bot = Bot(company_name="company_name", bot_name="GeniusBot")


failed_cases = []
total_cases_count = 100
for loop in range(total_cases_count):
    called = False
    conversion = []
    for message in messages:
        bot.console.user_print(message)
        conversion.append(message)
        response = bot.run(message)
        bot.console.ai_print(response["text"])
        conversion.append(response["text"])
        calling = response["function_calling"]
        __import__("pprint").pprint(calling)
        if calling:
            called = True
            __import__("pprint").pprint(calling)
    bot.memory.clear()
    print(
        "------------------------------------------------------------------------------------------------"
    )
    if not called:
        failed_cases.append(conversion)

failed_cases_count = len(failed_cases)


print(f"Failed cases count: {failed_cases_count}")
print(f"Failed cases count: {total_cases_count}")
# bot.run_interactively()
