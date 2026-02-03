"""
CLI Module

Command-line interface for DocuChat using Rich for beautiful output.
"""

import logging
from rich.console import Console
from rich.logging import RichHandler

# Configure rich logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger(__name__)
console = Console()


def main():
    """
    Main CLI entry point.
    
    TODO (Day 5):
    - Implement Click commands
    - Process command for document ingestion
    - Query command for Q&A
    - Interactive chat mode
    - Beautiful output with Rich
    """
    console.print("[bold green]DocuChat - Intelligent Document Q&A System[/bold green]")
    console.print("Version 0.1.0\n")
    
    console.print("[yellow]CLI not yet implemented. Coming on Day 5![/yellow]")
    console.print("\nPlanned commands:")
    console.print("  • docuchat process <directory>  - Process PDF documents")
    console.print("  • docuchat query <question>     - Ask a question")
    console.print("  • docuchat chat                 - Interactive chat mode")
    console.print("  • docuchat reset                - Clear vector database")


if __name__ == "__main__":
    main()
