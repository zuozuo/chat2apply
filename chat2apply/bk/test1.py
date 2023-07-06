from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
model = ChatOpenAI(model="gpt-3.5-turbo-0613")
from langchain.tools import MoveFileTool, format_tool_to_openai_function
tools = [MoveFileTool()]
functions = [format_tool_to_openai_function(t) for t in tools]
message = model.predict_messages(
    [HumanMessage(content="move file foo to bar")], functions=functions
)
