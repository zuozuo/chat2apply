from rich.console import Console

AI_TEXT_COLOR = 'bright_magenta'

class BotConsole():
    """console uitls for chatbot"""

    def __init__(self, name, console=None):
        self.name = name
        self.console = console or Console(highlight=False)

    def ai_print(self, text):
        self.console.print(f"[b]{self.name}[/b]: ", end="", style=AI_TEXT_COLOR)
        self.console.print(f"\n   {text}")

    def user_print(self, text):
        self.console.print(f"[b]You[/b]: ", end="", style=AI_TEXT_COLOR)
        self.console.print(f"\n   {text}")

    def get_user_input(self):
        return self.console.input("[b]You:[/b]\n   ").strip()

    def print_welcome_message(self):
        self.ai_print(
            f"I am {self.name}, an AI assistant to help you find and apply jobs. And you can also ask me question about company benefits and working environment."
        )
