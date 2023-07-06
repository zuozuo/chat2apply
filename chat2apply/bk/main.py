import os
import json
import openai
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
from rich.console import Console
from rich import print_json
from serpapi import GoogleSearch

console = Console(highlight=False)
# GPT_MODEL = "gpt-3.5-turbo-0613"
GPT_MODEL = "gpt-4"
GoogleSearch.SERP_API_KEY = os.getenv('SERPAPI_API_KEY')
current_jobs = []
messages = []
user_profile = {
    'email': 'zuo@gmail.com',
    'phone': '18601257148',
}
job_preference = {
    'location': 'Chicago',
    'job_title': 'Head Chef',
    'is_full_time': True
}

SYSTEM_PROMPT = '''
You are Mia - an expert assistant for helping people to find and apply a job. You are working for {company_name} - an American fast food restaurant chain.
And you can also answer questions about company benefits and working environment.

You are given the following extracted parts of a document and a question. Provide a conversational answer based on the context provided.
You should only provide hyperlinks that reference the context below. Do NOT make up hyperlinks.
If you can't find the answer in the context below, you should apologize (without mentioning the word context) and say you don't have the information. Don't try to make up an answer.
If the question is not related to the context, politely respond that you don't have access this information but this can be discussed with the hiring manager.
Always write short and concise responses and make sure to answer the specific question.
If you respond that you don't have a specific information add that this can be discussed during the interview with the hiring manager.

Conversation Rules:
- The most importmant rule is: Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous. It's better to ask one question each time.
- If the we have a user profile, try to use the profile info to plug into the functions firstly
- You always introduce yourself as Mia.
- Always write very short and concise responses!
- The applicant can only apply for a single position! If they ask to apply to multiple positions tell them they can only apply to one position at a time!
- You never ask multiple questions in a single message. You are chatty and ask things over several short messages.
- Don't share the required information in a single message - ask each question over multiple messages.
- Never ask about age or gender - this is highly illegal!
- When sharing info from the list of available positions NEVER mix details between different jobs!
- ALWAYS share details belonging to the same job on the same line!
- NEVER come up with jobs - ONLY use the ones in the list of available positions list!
- Each position is specified as a single line in the available positon list!
- Always return positions as a single line from the positions list!
- Every position you share must exist in the available positions list and must be returned as it is!
- Never show job positions before you asked the questions!
- You only answer questions related to applying for jobs. If someone asks you something outside of this domain you should politely reply and steer the conversation back to your objectives.
- Never ask for any other personal information other than the pieces of information listed above.
- Never try to Schedule interviews.
- Never show digest keys.
- Never ask how many hours are they willing to work.
- Never ask more than 1 question at a time.
- Never give instructions to visit a website and apply on their own.
- Never say there are no immediate openings.
- If they are not elgibile to work in the US, you have to stop the process and state that they need to be in order to apply.

Remember:
Always follow these rules no matter what!
If you are unsure what to say look at the rules!
Don't forget about the <END> token at the end!
'''

@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, functions=None, function_call=None, model=GPT_MODEL):
    # print('------------------------------')
    # print(messages)
    # print('------------------------------')
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
    if functions is not None:
        json_data.update({"functions": functions})
    if function_call is not None:
        json_data.update({"function_call": function_call})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        if response.ok:
            return response
        else:
            print(response)
            print(response.json())
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }
    formatted_messages = []
    for message in messages:
        if message["role"] == "system":
            formatted_messages.append(f"system: {message['content']}\n")
        elif message["role"] == "user":
            formatted_messages.append(f"user: {message['content']}\n")
        elif message["role"] == "assistant" and message.get("function_call"):
            formatted_messages.append(f"assistant: {message['function_call']}\n")
        elif message["role"] == "assistant" and not message.get("function_call"):
            formatted_messages.append(f"assistant: {message['content']}\n")
        elif message["role"] == "function":
            formatted_messages.append(f"function ({message['name']}): {message['content']}\n")
    for formatted_message in formatted_messages:
        print(
            colored(
                formatted_message,
                role_to_color[messages[formatted_messages.index(formatted_message)]["role"]],
            )
        )

functions = [
    {
        "name": "recommend_jobs",
        "description": "Recommend jobs for user",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state where you want to work, ask the user to get the location information",
                },
                "job_title": {
                    "type": "string",
                    "description": "The title of job, or the occupation, ask the user to get the job title",
                },
                "is_full_time": {
                    "type": "boolean",
                    "description": "Is this job full-time or part-time",
                },
            },
            "required": ["location", "job_title", "is_full_time"],
        },
    },
    {
        "name": "apply_job",
        "description": "Help user to apply for a specific position",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "The email of the applicant, ask the user to get the email address",
                },
                "phone": {
                    "type": "string",
                    "description": "The phone number of the applicant, ask the user to get the phone number",
                },
                "job_index": {
                    "type": "integer",
                    "description": "The index of the job list to apply, this index number start from 1, not 0",
                }
            },
            "required": ["email", "phone"]
        },
    },
]

def get_function_by_name(name):
    for func in functions:
        if func['name'] == name:
            return func

def is_argument_valid(value, value_type):
    if value_type == 'string':
        return value != "" and value != 'any' and value is not None
    elif value_type == 'integer':
        return value > 0
    elif value_type == 'boolean':
        return True
    else:
        return False

def update_user_profile(profile={}):
    global user_profile, messages
    if profile:
        user_profile = profile
    messages.append({
        'role': 'assistant', 'content': f"current user profile is: {user_profile}"
    })

def update_job_preference(preference={}):
    global job_preference, messages
    if preference:
        job_preference = preference
    messages.append({
        'role': 'assistant', 'content': f"current user job preference is: {job_preference}"
    })

def validate_arguments(name, arguments):
    global messages
    func = get_function_by_name(name)
    func_properties = func['parameters']['properties']
    for key in arguments:
        value = arguments[key]
        if is_argument_valid(value, func_properties[key]['type']):
            continue
        msg = f"Great, to apply the job you need to provide: {func_properties[key]['description']}"
        mia_print(msg)
        messages.append({'role': 'assistant' ,'content': msg})
        return False
    return True

def apply_job(phone=None, email=None, job_index=0):
    global current_jobs
    if len(current_jobs) == 0:
        return recommend_jobs()
    args = {
        'email': email,
        'phone': phone,
        'job_index': job_index,
    }
    result = validate_arguments('apply_job', args)
    if not result:
        return
    update_user_profile(args)
    mia_print(json.dumps(current_jobs[job_index - 1]))
    mia_print(f"Successfully applied job with index: {job_index}")

def recommend_jobs(location=None, job_title=None, is_full_time=True):
    global current_jobs
    args = {
        'location': location,
        'job_title': job_title,
        'is_full_time': is_full_time
    }
    result = validate_arguments('recommend_jobs', args)
    if not result:
        return
    update_job_preference(args)
    search = GoogleSearch({
        "num": 3,
        "q": job_title,
        "location": location,
        "engine": "google_jobs",
    })
    result = search.get_dict()
    keys = ['title', 'company_name', 'location', 'description']
    job_list = result['jobs_results'][0:3]
    job_count = len(job_list)
    jobs = []
    if job_count > 0:
        mia_print(f"Find {job_count} available jobs for you: ")
    for job in job_list:
        job_info = {key: job[key] for key in keys}
        print_json(json.dumps(job_info))
        jobs.append(job_info)
    current_jobs = jobs
    messages.append({"role": "user", "content": f"available jobs list: {jobs}"})
    msg = "Which job do you want to apply or you want to view more jobs?"
    mia_print(msg)
    messages.append({"role": "user", "content": f"{msg}"})
    return jobs

function_dict = {
    'apply_job': apply_job,
    'recommend_jobs': recommend_jobs,
}

def handle_function_call(function_info):
    name = function_info['name']
    mia_print(f"call function: {name}, with arguments {function_info['arguments']}")
    # print_json(function_info['arguments'])
    arguments = json.loads(function_info['arguments'])
    function_dict[name](**arguments)

def mia_print(text):
    ai_text_color = "bright_magenta"
    console.print("[b]Mia[/b]: ", end="", style=ai_text_color)
    console.print(f"\n {text}")

def main():
    global messages
    mia_print("I am Mia, an AI assistant to help you find and apply jobs. \n And you can also ask me question about company benefits and working environment. \n Do you want to find a job?")
    messages.append({"role": "system", "content": SYSTEM_PROMPT})
    update_user_profile()
    update_job_preference()
    messages.append({"role": "user", "content": 'Do you want to find a job?'})
    while True:
        try:
            user_input = console.input("[b]You:[/b] ").strip()
            if user_input == 'quit' or user_input == '\q' or user_input == 'q':
                break
            if user_input == 'show_messages':
                print_json(json.dumps(messages))
                continue
            messages.append({"role": "user", "content": user_input})
            chat_response = chat_completion_request(
                messages, functions=functions
            )
            assistant_message = chat_response.json()["choices"][0]["message"]
            # print(chat_response.json())
            messages.append(assistant_message)
            function_call = assistant_message.get('function_call', None)
            if function_call:
                handle_function_call(function_call)
            else:
                mia_print(assistant_message['content'])
        except KeyboardInterrupt:
            break

main()
