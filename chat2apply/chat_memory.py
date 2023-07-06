from typing import Any, Dict, Tuple

from langchain.memory import ConversationBufferMemory

class ChatMemory(ConversationBufferMemory):
    input_key: str = 'input'
    output_key: str = 'text'

    def _get_input_output(
        self, inputs: Dict[str, Any], outputs: Dict[str, str]
    ) -> Tuple[str, str]:
        return inputs[self.input_key], outputs[self.output_key]
