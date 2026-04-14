"""Utility functions for multi-agent systems."""
from colorama import Fore, Style, init
from typing import Optional

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def print_agent_message(agent_name: str, message: str, color: Optional[str] = None):
    """Print formatted agent message with color."""
    if color is None:
        color = Fore.CYAN
    
    print(f"\n{color}{'='*60}")
    print(f"{agent_name.upper()}")
    print(f"{'='*60}{Style.RESET_ALL}")
    print(f"{message}")
    print()

def print_section(title: str):
    """Print a section header."""
    print(f"\n{Fore.YELLOW}{'='*60}")
    print(f"{title.upper()}")
    print(f"{'='*60}{Style.RESET_ALL}\n")
