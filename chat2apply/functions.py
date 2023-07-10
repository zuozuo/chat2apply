# pylint: disable=line-too-long

import os
import json
from serpapi import GoogleSearch

GoogleSearch.SERP_API_KEY = os.getenv('SERPAPI_API_KEY')

function_specs = [
    {
        "name": "search_jobs",
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

def safe_parse_arguments(args_str):
    try:
        return json.loads(args_str)
    except Exception as e:
        raise ValueError(f"invalid function_call arguments: {args_str}") from e

def parse_function_call(params):
    name = params.get('name') or ''
    _args = params.get('arguments') or '{}'
    args = safe_parse_arguments(_args)
    if is_function_valid(name):
        return name, args
    raise ValueError(f"invalid function: name={name} params={params}")

def get_func_spec(name):
    for spec in function_specs:
        if spec['name'] == name:
            return spec
    return {}

def is_function_valid(name):
    spec = get_func_spec(name)
    return bool(spec)

def is_argument_valid(value, value_type):
    if value_type == 'string':
        return value != "" and value != 'any' and value is not None
    if value_type == 'integer':
        return value > 0
    if value_type == 'boolean':
        return True
    return False

def find_invalid_argument(name, arguments):
    spec = get_func_spec(name)
    func_properties = spec['parameters']['properties']
    for key in arguments:
        value = arguments[key]
        if is_argument_valid(value, func_properties[key]['type']):
            continue
        return {
            'name': key,
            'properties': func_properties[key]
        }
    return {}

def search_jobs(args):
    search = GoogleSearch({
        "num": 3,
        "q": args.get('job_title'),
        "location": args.get('location'),
        "engine": "google_jobs",
    })
    result = search.get_dict()
    keys = ['title', 'company_name', 'location', 'description']
    job_list = result['jobs_results'][0:3]
    jobs = []
    for job in job_list:
        job_info = {key: job[key] for key in keys}
        jobs.append(job_info)
    return jobs

def apply_job(args):
    import ipdb; ipdb.set_trace(context=5)
    return args
