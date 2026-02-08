"""Main entry point for the Todo CLI application."""

import sys
from typing import Optional

from src.cli.parser import parse_args
from src.cli.commands.help import run_help
from src.cli.commands.add import run_add
from src.cli.commands.list import run_list
from src.cli.commands.search import run_search
from src.cli.commands.update import run_update
from src.cli.commands.complete import run_complete
from src.cli.commands.delete import run_delete
from src.cli.commands.check_due import run_check_due
from src.cli.commands.dismiss import run_dismiss
from src.lib.errors import TodoError
from src.lib.storage import storage
from src.lib.display import format_reminder_list
from src.services.reminder import get_startup_reminders


def show_startup_reminders():
    """
    Show reminders on application startup.

    Displays tasks with upcoming or overdue due dates.
    Only shown when there are reminders to display.
    """
    tasks = storage.get_all()
    if not tasks:
        return

    reminder_tasks = get_startup_reminders(tasks)
    if reminder_tasks:
        print("\n" + "=" * 60)
        print("REMINDERS")
        print(format_reminder_list(reminder_tasks))
        print("=" * 60 + "\n")


def run_command(args) -> str:
    """
    Execute the appropriate command based on parsed arguments.

    Args:
        args: Parsed command line arguments

    Returns:
        Command output string
    """
    command = args.command

    if command == "help":
        return run_help(args.topic if hasattr(args, "topic") else None)

    elif command == "add":
        title = " ".join(args.title) if isinstance(args.title, list) else args.title
        return run_add(
            title=title,
            priority=args.priority,
            category=args.category,
            due=args.due,
            recur=args.recur,
        )

    elif command == "list":
        return run_list(
            status=args.status,
            priority=args.priority,
            category=args.category,
            sort=args.sort,
            order=args.order,
        )

    elif command == "search":
        return run_search(keyword=args.keyword)

    elif command == "update":
        return run_update(
            task_id=args.id,
            title=args.title,
            priority=args.priority,
            category=args.category,
            due=args.due,
            recur=args.recur,
        )

    elif command == "complete":
        return run_complete(task_id=args.id)

    elif command == "delete":
        return run_delete(task_id=args.id)

    elif command == "check-due":
        return run_check_due()

    elif command == "dismiss":
        return run_dismiss(task_id=args.id)

    else:
        return run_help()


def main(argv: Optional[list[str]] = None) -> int:
    """
    Main entry point for the CLI application.

    Args:
        argv: Command line arguments (defaults to sys.argv)

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        args = parse_args(argv)

        # Show startup reminders for commands that display task data
        # (but not for help, add, or other utility commands)
        if args.command in ["list", "check-due"]:
            pass  # Reminders shown inline with these commands
        elif args.command not in ["help", None]:
            # For other commands, show reminders briefly
            show_startup_reminders()

        result = run_command(args)
        print(result)
        return 0

    except TodoError as e:
        print(e.user_message())
        return 1

    except SystemExit:
        # argparse calls sys.exit on --help or errors
        return 0

    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return 1

    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
