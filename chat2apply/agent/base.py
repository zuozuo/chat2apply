class BaseAgent(object):
    """Base agent class for custom agent"""

    # for more information about function calling feature's function specs definition please refer to:
    # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb
    @property
    def function_specs(self):
        raise NotImplementedError

    @property
    def name(self):
        return self.function_specs.get("name", "")


    # when function calling is triggered, run this function
    def run(self, args):
        raise NotImplementedError

    # this function is called after the run function
    def callback(self, result, bot):
        raise NotImplementedError
