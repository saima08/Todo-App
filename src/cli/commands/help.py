"""Help command implementation."""

from src.cli.parser import create_parser, get_command_help


GENERAL_HELP = """
Todo CLI - Task Management Application
======================================

A command-line todo list manager with task organization, search, filter,
sort, due dates, and recurring task support.

USAGE:
    todo <command> [options]

COMMANDS:
    add         Add a new task
    list        List all tasks (with optional filters and sorting)
    search      Search tasks by keyword
    update      Update an existing task
    complete    Toggle task completion status
    delete      Delete a task
    check-due   Show tasks with upcoming or overdue due dates
    dismiss     Dismiss reminder for a task
    help        Show this help message

QUICK START:
    todo add "Buy groceries"                    # Add a simple task
    todo add "Report" -p high -c work           # Add with priority and category
    todo list                                   # Show all tasks
    todo list --status incomplete               # Show only incomplete tasks
    todo complete 1                             # Mark task #1 as complete
    todo delete 1                               # Delete task #1

OPTIONS:
    --help, -h    Show help for a specific command

EXAMPLES:
    todo add "Project deadline" --priority high --category work --due 2026-02-15
    todo list --priority high --sort due --order asc
    todo search --keyword project
    todo update 1 --title "Updated title" --priority medium

For more details on a command, use: todo help <command>
"""


def run_help(topic: str = None) -> str:
    """
    Display help information.

    Args:
        topic: Optional command name to get specific help

    Returns:
        Help text to display
    """
    if topic is None:
        return GENERAL_HELP

    try:
        return get_command_help(topic)
    except Exception:
        return f"No help available for '{topic}'. Use 'todo help' for general help."
