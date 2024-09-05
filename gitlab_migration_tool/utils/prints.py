from rich.console import Console
from rich.text import Text

console = Console()

def print_styled_message(message):
    text = Text(message, style="dim cyan")
    console.print(text)
    
def print_error_message(message):
    error_text = Text(message, style="bold red")
    console.print(error_text)
    
def print_warning_message(message):
    error_text = Text(message, style="bold yellow")
    console.print(error_text)
    
def print_success_message(message):
    error_text = Text(message, style="bold green")
    console.print(error_text)
