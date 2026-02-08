# Tasks: CLI-Based Todo Application Phase I

**Input**: Design documents from `/specs/01-cli-todo-phase1/`
**Prerequisites**: plan.md (loaded), spec.md (loaded)
**Branch**: `01-cli-todo-phase1`
**Created**: 2026-02-05

**Tests**: No test tasks included (not explicitly requested in spec). Add test tasks if TDD approach is desired.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md structure (Single CLI project):

```text
src/
├── models/         # Data entities
├── services/       # Business logic
├── cli/            # CLI commands and parsing
└── lib/            # Shared utilities

tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
└── contract/       # Contract tests
```

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure per plan.md (src/models, src/services, src/cli, src/lib, tests/)
- [x] T002 Initialize project with chosen language/framework and dependencies
- [x] T003 [P] Configure linting and formatting tools
- [x] T004 [P] Create README.md with project overview and CLI usage instructions
- [x] T005 [P] Setup entry point for CLI application in src/cli/main.py (or equivalent)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Define Task entity with all fields in src/models/task.py (ID, title, status, priority, category, due_date, recurrence, created_at, modified_at)
- [x] T007 [P] Create in-memory storage manager in src/lib/storage.py (task list, ID generation, CRUD operations)
- [x] T008 [P] Create CLI argument parser framework in src/cli/parser.py (command routing, help system)
- [x] T009 [P] Implement error handling utilities in src/lib/errors.py (user-friendly error messages)
- [x] T010 [P] Create display formatter utilities in src/lib/display.py (tabular output, visual indicators)
- [x] T011 Implement help command in src/cli/commands/help.py (displays all available commands)

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add and Manage Basic Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create, view, update, delete tasks and toggle completion status

**Independent Test**: Create multiple tasks, view list, update a task, mark complete, delete a task - all operations should work with appropriate feedback and error handling

**Acceptance Criteria** (from spec.md):
- AS-1.1: Add task with title → appears with auto-generated ID and incomplete status
- AS-1.2: View task list → shows ID, title, completion status, details
- AS-1.3: Update task title → title changes and visible in list
- AS-1.4: Mark task complete → status changes, visually distinguished
- AS-1.5: Delete task → removed from list

### Implementation for User Story 1

- [x] T012 [US1] Implement `add` command in src/cli/commands/add.py (FR-001, FR-006)
- [x] T013 [US1] Implement `list` command in src/cli/commands/list.py (FR-004, FR-007)
- [x] T014 [US1] Implement `update` command in src/cli/commands/update.py (FR-003)
- [x] T015 [US1] Implement `complete` command in src/cli/commands/complete.py (FR-005)
- [x] T016 [US1] Implement `delete` command in src/cli/commands/delete.py (FR-002, FR-008)
- [x] T017 [US1] Add validation for empty title rejection in src/cli/commands/add.py (Edge Case)
- [x] T018 [US1] Add validation for invalid ID errors in src/cli/commands/update.py and delete.py (Edge Cases)
- [x] T019 [US1] Add "No tasks found" message handling in src/cli/commands/list.py (Edge Case)
- [x] T020 [US1] Wire all US1 commands to CLI parser in src/cli/parser.py

**Checkpoint**: User Story 1 complete - Basic CRUD operations functional. This is the MVP!

---

## Phase 4: User Story 2 - Organize Tasks with Priorities and Categories (Priority: P2)

**Goal**: Enable users to assign priority levels (high/medium/low) and categories (work/home/personal) to tasks

**Independent Test**: Create tasks with priorities and categories, verify attributes display correctly with visual distinction

**Acceptance Criteria** (from spec.md):
- AS-2.1: Assign priority and category on create → attributes visible in list
- AS-2.2: View list → priority levels visually distinguished
- AS-2.3: View list → category labels visible
- AS-2.4: Update task → priority/category attributes updated

### Implementation for User Story 2

- [x] T021 [P] [US2] Add priority enum (high/medium/low) to src/models/task.py (FR-009)
- [x] T022 [P] [US2] Add category enum (work/home/personal) to src/models/task.py (FR-010)
- [x] T023 [US2] Extend `add` command to accept --priority and --category flags in src/cli/commands/add.py
- [x] T024 [US2] Extend `update` command to accept --priority and --category flags in src/cli/commands/update.py
- [x] T025 [US2] Update `list` display to show priority with visual distinction in src/lib/display.py (FR-011)
- [x] T026 [US2] Update `list` display to show category labels in src/lib/display.py (FR-011)
- [x] T027 [US2] Update help documentation for priority/category options in src/cli/commands/help.py

**Checkpoint**: User Story 2 complete - Tasks can be organized with priorities and categories

---

## Phase 5: User Story 3 - Search and Filter Tasks (Priority: P2)

**Goal**: Enable users to search by keyword and filter by status, priority, or category

**Independent Test**: Create tasks with various attributes, search by keyword, filter by each criterion, verify correct results returned with count

**Acceptance Criteria** (from spec.md):
- AS-3.1: Search by keyword → only matching tasks shown
- AS-3.2: Filter by status → only matching status shown
- AS-3.3: Filter by priority → only matching priority shown
- AS-3.4: Filter by category → only matching category shown
- AS-3.5: Clear filter → all tasks visible again

### Implementation for User Story 3

- [x] T028 [P] [US3] Implement search service in src/services/search.py (keyword matching in titles) (FR-012)
- [x] T029 [P] [US3] Implement filter service in src/services/filter.py (status, priority, category filters) (FR-013, FR-014, FR-015)
- [x] T030 [US3] Implement `search` command in src/cli/commands/search.py with --keyword flag
- [x] T031 [US3] Extend `list` command to accept --status, --priority, --category filter flags in src/cli/commands/list.py
- [x] T032 [US3] Add result count display to search and filter results in src/lib/display.py (FR-018)
- [x] T033 [US3] Add "No matching tasks" message for empty search/filter results (Edge Cases)
- [x] T034 [US3] Update help documentation for search/filter options in src/cli/commands/help.py

**Checkpoint**: User Story 3 complete - Search and filter functionality operational

---

## Phase 6: User Story 4 - Sort Tasks (Priority: P2)

**Goal**: Enable users to sort tasks by title or priority in ascending/descending order

**Independent Test**: Create tasks with different priorities and titles, apply sort options, verify correct order

**Acceptance Criteria** (from spec.md):
- AS-4.1: Sort by priority → high first, then medium, then low
- AS-4.2: Sort alphabetically → A-Z order by title
- AS-4.3: Change sort criteria → order updates accordingly

### Implementation for User Story 4

- [x] T035 [P] [US4] Implement sort service in src/services/sort.py (title, priority sorting) (FR-016, FR-017)
- [x] T036 [US4] Extend `list` command to accept --sort and --order flags in src/cli/commands/list.py
- [x] T037 [US4] Implement stable sort for identical values (secondary sort by ID) in src/services/sort.py (Edge Case)
- [x] T038 [US4] Update help documentation for sort options in src/cli/commands/help.py

**Checkpoint**: User Story 4 complete - Sort functionality operational

---

## Phase 7: User Story 5 - Track Due Dates and Receive Reminders (Priority: P3)

**Goal**: Enable users to set due dates, view reminders, and receive alerts for approaching/overdue tasks

**Independent Test**: Create tasks with due dates, verify display, check reminder intervals, verify overdue highlighting

**Acceptance Criteria** (from spec.md):
- AS-5.1: Set due date on create → due date visible in list
- AS-5.2: Sort by due date → chronological order
- AS-5.3: Approaching due date → visual highlight for urgency

**Additional FR Coverage**:
- FR-021: Two reminder mechanisms (check-due command + app start)
- FR-021a: Escalating intervals (7/3/1 days, on due date)
- FR-021b: Overdue tasks highlighted differently
- FR-021c: Dismiss/clear reminder functionality
- FR-021d: Days until/overdue display
- FR-021e: Reminders only for incomplete tasks

### Implementation for User Story 5

- [x] T039 [P] [US5] Add due_date field handling to Task model in src/models/task.py (FR-019)
- [x] T040 [P] [US5] Implement reminder calculation service in src/services/reminder.py (interval logic: 7/3/1/0 days) (FR-021a)
- [x] T041 [US5] Extend `add` command to accept --due flag in src/cli/commands/add.py
- [x] T042 [US5] Extend `update` command to accept --due flag in src/cli/commands/update.py
- [x] T043 [US5] Update `list` display to show due dates in src/lib/display.py (FR-020)
- [x] T044 [US5] Implement `check-due` command in src/cli/commands/check_due.py (FR-021)
- [x] T045 [US5] Implement app-start reminder display in src/cli/main.py (FR-021)
- [x] T046 [US5] Add visual highlighting for approaching due dates in src/lib/display.py (FR-025)
- [x] T047 [US5] Add distinct visual highlighting for overdue tasks in src/lib/display.py (FR-021b)
- [x] T048 [US5] Add "Due in X days" / "X days overdue" formatting in src/lib/display.py (FR-021d)
- [x] T049 [US5] Implement reminder dismissal tracking in src/services/reminder.py (FR-021c)
- [x] T050 [US5] Filter reminders to exclude completed tasks in src/services/reminder.py (FR-021e)
- [x] T051 [US5] Extend sort service for due date sorting in src/services/sort.py (FR-026)
- [x] T052 [US5] Handle past due dates (mark as overdue immediately) in src/services/reminder.py (Edge Case)
- [x] T053 [US5] Update help documentation for due date options in src/cli/commands/help.py

**Checkpoint**: User Story 5 complete - Due date tracking and reminder system operational

---

## Phase 8: User Story 6 - Manage Recurring Tasks (Priority: P3)

**Goal**: Enable users to create recurring tasks (daily/weekly/monthly) that automatically create new instances on completion

**Independent Test**: Create recurring task, complete it, verify new instance created with advanced due date

**Acceptance Criteria** (from spec.md):
- AS-6.1: Complete recurring task → new instance appears with due date advanced
- AS-6.2: Daily recurrence → task visible each day with current day's due date
- AS-6.3: Update recurrence schedule → future instances follow new schedule

### Implementation for User Story 6

- [x] T054 [P] [US6] Add recurrence_schedule enum (none/daily/weekly/monthly) to src/models/task.py (FR-022)
- [x] T055 [P] [US6] Implement recurrence service in src/services/recurrence.py (schedule calculation, instance creation) (FR-023)
- [x] T056 [US6] Extend `add` command to accept --recur flag in src/cli/commands/add.py
- [x] T057 [US6] Extend `update` command to accept --recur flag in src/cli/commands/update.py (FR-024)
- [x] T058 [US6] Modify `complete` command to trigger recurrence logic in src/cli/commands/complete.py
- [x] T059 [US6] Update `list` display to show recurrence indicator in src/lib/display.py
- [x] T060 [US6] Handle overdue recurring task (show as overdue, no new instance until completion) in src/services/recurrence.py (Edge Case)
- [x] T061 [US6] Update help documentation for recurrence options in src/cli/commands/help.py

**Checkpoint**: User Story 6 complete - Recurring task functionality operational

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T062 [P] Review and update all help documentation in src/cli/commands/help.py
- [x] T063 [P] Code cleanup and consistent error messaging across all commands
- [x] T064 [P] Verify command syntax consistency across all CLI commands
- [x] T065 Ensure accessible output (text-only, color-independent information) in src/lib/display.py
- [x] T066 Final validation: Run all acceptance scenarios from spec.md manually
- [x] T067 Update README.md with complete command reference

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Foundational (BLOCKS all user stories)
    ↓
    ├── Phase 3: US1 (P1) 🎯 MVP ──────────────────────┐
    │                                                   │
    ├── Phase 4: US2 (P2) ──┐                          │
    │                       │                          │
    ├── Phase 5: US3 (P2) ──┼── Can run in parallel   │
    │                       │   after US1 complete    │
    ├── Phase 6: US4 (P2) ──┘                          │
    │                                                   │
    ├── Phase 7: US5 (P3) ──┐                          │
    │                       │── Can run in parallel   │
    └── Phase 8: US6 (P3) ──┘                          │
                                                       ↓
                                            Phase 9: Polish
```

### User Story Dependencies

| User Story | Can Start After | Dependencies | Notes |
|------------|-----------------|--------------|-------|
| US1 (P1) | Phase 2 | None | MVP - start first |
| US2 (P2) | US1 | Extends add/update commands | Build on US1 |
| US3 (P2) | US1 | Uses Task model, list command | Independent of US2 |
| US4 (P2) | US1 | Uses Task model, list command | Independent of US2, US3 |
| US5 (P3) | US1 | Extends Task model, commands | Independent of US2-4 |
| US6 (P3) | US1, US5 (partial) | Uses due date from US5 | Benefits from US5 but can work without |

### Within Each User Story

1. Model changes first (if any)
2. Service layer implementation
3. CLI command implementation
4. Display/formatting updates
5. Help documentation updates
6. Edge case handling

### Parallel Opportunities

**Phase 1 (Setup)**:
- T003, T004, T005 can run in parallel

**Phase 2 (Foundational)**:
- T007, T008, T009, T010 can run in parallel after T006

**Within User Stories**:
- Model/enum additions marked [P] can run in parallel
- Service implementations marked [P] can run in parallel

**Across User Stories** (after US1 complete):
- US2, US3, US4 can be developed in parallel
- US5, US6 can be developed in parallel

---

## Parallel Example: Phase 2 (Foundational)

```bash
# Sequential (blocking):
T006: Define Task entity (must be first)

# Then parallel:
T007: Create in-memory storage manager
T008: Create CLI argument parser framework
T009: Implement error handling utilities
T010: Create display formatter utilities

# Then:
T011: Implement help command (depends on T008)
```

## Parallel Example: User Story 2

```bash
# Parallel model updates:
T021: Add priority enum to Task model
T022: Add category enum to Task model

# Then sequential command updates:
T023: Extend add command
T024: Extend update command
T025: Update list display for priority
T026: Update list display for category
T027: Update help documentation
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. ✅ Complete Phase 1: Setup (T001-T005)
2. ✅ Complete Phase 2: Foundational (T006-T011)
3. ✅ Complete Phase 3: User Story 1 (T012-T020)
4. **STOP and VALIDATE**: Test all basic CRUD operations
5. Deploy/demo if ready - This is the MVP!

### Incremental Delivery

| Increment | User Stories | Value Delivered |
|-----------|--------------|-----------------|
| MVP | US1 | Basic task management (CRUD) |
| +Organization | US2, US3, US4 | Priority, category, search, filter, sort |
| +Intelligence | US5, US6 | Due dates, reminders, recurring tasks |
| Final | Polish | Polished, documented, accessible |

### Success Criteria Mapping

| Success Criteria | User Stories | Tasks |
|------------------|--------------|-------|
| SC-001 | US1 | T012-T020 |
| SC-002 | US2, US3, US4 | T021-T038 |
| SC-003 | US1 | T011, T012-T020 |
| SC-004 | US1 | T007 (storage capacity) |
| SC-005 | US3 | T028-T034 |
| SC-006 | US6 | T054-T061 |
| SC-007, SC-008, SC-009, SC-010 | US5 | T039-T053 |

---

## Task Summary

| Phase | Description | Task Count | Parallel Tasks |
|-------|-------------|------------|----------------|
| Phase 1 | Setup | 5 | 3 |
| Phase 2 | Foundational | 6 | 4 |
| Phase 3 | US1 - Basic CRUD (P1) 🎯 MVP | 9 | 0 |
| Phase 4 | US2 - Priority/Category (P2) | 7 | 2 |
| Phase 5 | US3 - Search/Filter (P2) | 7 | 2 |
| Phase 6 | US4 - Sort (P2) | 4 | 1 |
| Phase 7 | US5 - Due Dates/Reminders (P3) | 15 | 2 |
| Phase 8 | US6 - Recurring Tasks (P3) | 8 | 2 |
| Phase 9 | Polish | 6 | 3 |
| **Total** | | **67** | **19** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- No test tasks included - add them if TDD approach is desired
- All functional requirements (FR-001 to FR-026) are covered
- All edge cases from spec.md are addressed

---

**Generated**: 2026-02-05 | **Tasks Version**: 1.0.0
