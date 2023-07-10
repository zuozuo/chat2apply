from rich.console import Console

AI_TEXT_COLOR = 'bright_magenta'
USER_TEXT_COLOR = 'cyan'
SYSTEM_TEXT_COLOR = 'blue'
from .prompts import WELCOME_MESSAGE

class BotConsole():
    """console uitls for chatbot"""

    def __init__(self, name, console=None):
        self.name = name
        self.console = console or Console(highlight=False)

    def ai_print(self, text):
        self.console.print(f"[b]{self.name}[/b]: ", end="", style=AI_TEXT_COLOR)
        self.console.print(f"\n   {text}")

    def user_print(self, text):
        self.console.print(f"[b]You[/b]: ", end="", style=USER_TEXT_COLOR)
        self.console.print(f"\n   {text}")

    def system_print(self, text):
        self.console.print(f"[b]System[/b]: ", end="", style=SYSTEM_TEXT_COLOR)
        self.console.print(f"\n   {text}")

    def get_user_input(self):
        return self.console.input("[b]You:[/b]\n   ").strip()

    def print_welcome_message(self):
        self.ai_print(WELCOME_MESSAGE.format(name=self.name))
