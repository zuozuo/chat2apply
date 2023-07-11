import os
from serpapi import GoogleSearch

from .base import BaseAgent

GoogleSearch.SERP_API_KEY = os.getenv("SERPAPI_API_KEY")


class SearchJobAgent(BaseAgent):
    @property
    def function_specs(self):
        return {
            "name": "search_jobs",
            "description": "Recommend jobs for user",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state where you want to work, ask the user to get the location information",  # noqa: E501
                    },
                    "job_title": {
                        "type": "string",
                        "description": "The title of job, or the occupation, ask the user to get the job title",  # noqa: E501
                    },
                    "is_full_time": {
                        "type": "boolean",
                        "description": "Is this job full-time or part-time",
                    },
                },
                "required": ["location", "job_title", "is_full_time"],
            },
        }

    def run(self, args):
        search = GoogleSearch(
            {
                "num": 3,
                "q": args.get("job_title"),
                "location": args.get("location"),
                "engine": "google_jobs",
            }
        )
        result = search.get_dict()
        keys = ["title", "company_name", "location", "description"]
        job_list = result["jobs_results"][0:3]
        jobs = []
        for job in job_list:
            job_info = {key: job[key] for key in keys}
            jobs.append(job_info)
        return jobs

    # this function only used in the interactively mode
    def callback(self, jobs, bot):
        # TODO: save jobs to current_jobs
        # TODO: save current pagination
        bot.print_and_save(f"available jobs list: {jobs}")
        bot.print_and_save(
            "Which job do you want to apply or you want to view more jobs?"
        )
