---
id: 03
title: Cross-Artifact Analysis Blocked Missing Tasks
stage: misc
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: cli-todo-phase1
branch: master
user: system
command: /sp.analyze
labels: ["analysis", "blocked", "prerequisite-missing"]
links:
  spec: specs/01-cli-todo-phase1/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - null
tests:
  - null
---

## Prompt

/sp.analyze

Goal: Identify inconsistencies, duplications, ambiguities, and underspecified items across the three core artifacts (spec.md, plan.md, tasks.md) before implementation.

## Response snapshot

Analysis aborted due to missing prerequisite artifact.

**Prerequisite Check Results**:
- spec.md: EXISTS at specs/01-cli-todo-phase1/spec.md
- plan.md: EXISTS at specs/01-cli-todo-phase1/plan.md
- tasks.md: MISSING - required for analysis

The /sp.analyze command requires all three core SDD artifacts to perform cross-artifact consistency analysis. Without tasks.md, the following analysis passes cannot be performed:
- Coverage gap detection (requirements with zero tasks)
- Task-to-requirement mapping
- Unmapped task identification
- Task ordering contradiction detection

**Recommendation**: Run /sp.tasks first to generate the task breakdown from the implementation plan, then re-run /sp.analyze.

## Outcome

- ✅ Impact: None - Analysis blocked, no findings produced
- 🧪 Tests: N/A
- 📁 Files: No files created or modified (read-only analysis)
- 🔁 Next prompts: /sp.tasks (required), then /sp.analyze
- 🧠 Reflection: Correct behavior - analysis should not proceed without complete artifact set

## Evaluation notes (flywheel)

- Failure modes observed: Prerequisite check correctly identified missing tasks.md
- Graders run and results (PASS/FAIL): Prerequisite gate FAIL (expected)
- Prompt variant (if applicable): Standard /sp.analyze workflow
- Next experiment (smallest change to try): N/A - run /sp.tasks first
