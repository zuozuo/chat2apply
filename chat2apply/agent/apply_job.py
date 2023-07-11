from .base import BaseAgent

class ApplyJobAgent(BaseAgent):
    @property
    def function_specs(self):
        return {
            "name": "apply_job",
            "description": "Help user to apply for a specific position",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The email of the applicant, ask the user to get the email address",  # noqa: E501
                    },
                    "phone": {
                        "type": "string",
                        "description": "The phone number of the applicant, ask the user to get the phone number",  # noqa: E501
                    },
                    "job_index": {
                        "type": "integer",
                        "description": "The index of the job list to apply, this index number start from 1, not 0",  # noqa: E501
                    }
                },
                "required": ["email", "phone"]
            },
        }

    def run(self, args):
        return args

    # this function only used in the interactively mode
    def callback(self, job, bot):
        bot.logger.info(job)
        bot.print_and_save(f"job={job} appled successfully!")
