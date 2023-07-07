from pydantic import BaseModel

from langchain.schema import BaseMessage, HumanMessage, SystemMessage, AIMessage

# if you want to save the chat history to database, just subclass this class
class ChatMemory(BaseModel):

    messages: list[BaseMessage] = []

    def add_message(self, message):
        self.messages.append(message)

    def add_user_message(self, message):
        self.add_message(HumanMessage(content=message))

    def add_ai_message(self, message):
        self.add_message(AIMessage(content=message))

    def add_system_message(self, message):
        self.add_message(SystemMessage(content=message))

    def clear(self):
        self.messages.clear()

    def load_history_messages(self):
        # subclass the ChatMemory class and implement this
        raise NotImplementedError()
