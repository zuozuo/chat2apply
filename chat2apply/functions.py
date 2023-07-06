class Functions:
    """function definitions for OpenAI function calling feature"""

    function_specs = [
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

    def __init__(self, model):
        self.model = model

    def functions(self):
        return {
            'apply_job': self.apply_job,
            'recommend_jobs': self.recommend_jobs,
        }

    def get_function_by_name(name):
        for func in self.functions():
            if func['name'] == name:
            return func
        return None

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
