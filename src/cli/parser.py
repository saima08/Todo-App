"""CLI argument parser framework for the Todo application."""

import argparse
import sys
from typing import Optional

from src.lib.errors import InvalidCommandError


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="todo",
        description="CLI-based Todo Application - Manage your tasks efficiently",
        epilog="Use 'todo <command> --help' for more information on a command.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", nargs="+", help="Task title")
    add_parser.add_argument(
        "--priority", "-p",
        choices=["high", "medium", "low"],
        help="Task priority level"
    )
    add_parser.add_argument(
        "--category", "-c",
        choices=["work", "home", "personal"],
        help="Task category"
    )
    add_parser.add_argument(
        "--due", "-d",
        help="Due date (YYYY-MM-DD format)"
    )
    add_parser.add_argument(
        "--recur", "-r",
        choices=["none", "daily", "weekly", "monthly"],
        help="Recurrence schedule"
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "--status", "-s",
        choices=["complete", "incomplete", "all"],
        default="all",
        help="Filter by completion status"
    )
    list_parser.add_argument(
        "--priority", "-p",
        choices=["high", "medium", "low"],
        help="Filter by priority"
    )
    list_parser.add_argument(
        "--category", "-c",
        choices=["work", "home", "personal"],
        help="Filter by category"
    )
    list_parser.add_argument(
        "--sort",
        choices=["id", "title", "priority", "due"],
        default="id",
        help="Sort by field"
    )
    list_parser.add_argument(
        "--order",
        choices=["asc", "desc"],
        default="asc",
        help="Sort order"
    )

    # Search command
    search_parser = subparsers.add_parser("search", help="Search tasks by keyword")
    search_parser.add_argument(
        "--keyword", "-k",
        required=True,
        help="Search keyword"
    )

    # Update command
    update_parser = subparsers.add_parser("update", help="Update an existing task")
    update_parser.add_argument("id", type=int, help="Task ID to update")
    update_parser.add_argument(
        "--title", "-t",
        help="New task title"
    )
    update_parser.add_argument(
        "--priority", "-p",
        choices=["high", "medium", "low", "none"],
        help="New priority level (use 'none' to clear)"
    )
    update_parser.add_argument(
        "--category", "-c",
        choices=["work", "home", "personal", "none"],
        help="New category (use 'none' to clear)"
    )
    update_parser.add_argument(
        "--due", "-d",
        help="New due date (YYYY-MM-DD format, or 'none' to clear)"
    )
    update_parser.add_argument(
        "--recur", "-r",
        choices=["none", "daily", "weekly", "monthly"],
        help="New recurrence schedule"
    )

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Toggle task completion")
    complete_parser.add_argument("id", type=int, help="Task ID to toggle")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID to delete")

    # Check-due command
    subparsers.add_parser("check-due", help="Show tasks with upcoming or overdue due dates")

    # Dismiss command (for reminder dismissal)
    dismiss_parser = subparsers.add_parser("dismiss", help="Dismiss reminder for a task")
    dismiss_parser.add_argument("id", type=int, help="Task ID to dismiss reminder")

    # Help command
    help_parser = subparsers.add_parser("help", help="Show help information")
    help_parser.add_argument(
        "topic",
        nargs="?",
        choices=["add", "list", "search", "update", "complete", "delete", "check-due", "dismiss"],
        help="Command to get help for"
    )

    return parser


def parse_args(args: Optional[list[str]] = None) -> argparse.Namespace:
    """
    Parse command line arguments.

    Args:
        args: Arguments to parse (defaults to sys.argv)

    Returns:
        Parsed namespace
    """
    parser = create_parser()

    if args is None:
        args = sys.argv[1:]

    # Handle empty args
    if not args:
        parser.print_help()
        sys.exit(0)

    return parser.parse_args(args)


def get_command_help(command: str) -> str:
    """Get detailed help for a specific command."""
    parser = create_parser()

    # Find the subparser for the command
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            if command in action.choices:
                subparser = action.choices[command]
                return subparser.format_help()

    raise InvalidCommandError(command)
