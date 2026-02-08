# Todo CLI Application

A command-line todo list manager with task organization, search, filter, sort, due dates, and recurring task support.

## Features

- **Basic Task Management**: Create, view, update, delete, and complete tasks
- **Organization**: Priority levels (high/medium/low) and categories (work/home/personal)
- **Search & Filter**: Find tasks by keyword, filter by status/priority/category
- **Sorting**: Sort by title, priority, or due date
- **Due Dates**: Set due dates with reminder alerts
- **Recurring Tasks**: Daily, weekly, or monthly recurring tasks

## Installation

```bash
# Install in development mode
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

## Usage

```bash
# Add a new task
todo add "Buy groceries"
todo add "Project report" --priority high --category work --due 2026-02-15

# List all tasks
todo list
todo list --status incomplete
todo list --priority high
todo list --category work
todo list --sort priority --order desc

# Search tasks
todo search --keyword groceries

# Update a task
todo update 1 --title "Buy groceries and milk"
todo update 1 --priority medium --category personal

# Mark task as complete
todo complete 1

# Delete a task
todo delete 1

# Check due dates
todo check-due

# Get help
todo help
todo help add
```

## Task Limits

- Maximum 1000 tasks supported (in-memory storage)
- Task titles: maximum 200 characters

## Requirements

- Python 3.11 or higher

## License

MIT License
