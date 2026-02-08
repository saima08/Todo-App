<!--
Sync Impact Report
Version change: [none] → 1.0.0
Modified principles: All principles added (new constitution)
Added sections: Core Principles, Agent Responsibilities, Constraints, Governance
Removed sections: None (template placeholders removed)
Templates requiring updates: ✅ spec-template.md, ✅ plan-template.md, ✅ tasks-template.md
Follow-up TODOs: None
-->

# Hackathon II – The Evolution of Todo Constitution

## Core Principles

### I. Specification Before Implementation
All work in Phase-1 must result in written specifications, not executable artifacts. The "what" must always be defined before the "how". No application code, configuration files, or pseudo-code resembling real logic is permitted during Phase-1. Specifications serve as the single source of truth and must be implementation-agnostic.

**Rationale**: Prevents premature optimization and ensures clear understanding before construction begins. Creates a durable artifact that outlives implementation choices.

### II. Clarity Over Completeness
Specifications must be unambiguous, human-readable, and free of implicit assumptions. Every requirement must be explicit. Ambiguity is considered a defect that blocks progression to Phase-2.

**Rationale**: Unclear specifications lead to implementation errors and rework. A clear incomplete spec is more valuable than a comprehensive confusing one.

### III. Single Source of Truth
Once approved, specifications are authoritative. All design decisions, user stories, requirements, and contracts must reside in the specification documents. No parallel documentation systems are permitted.

**Rationale**: Eliminates inconsistencies between documents and ensures all stakeholders reference the same information.

## Agent Responsibilities

### SpecAuthoringAgent
May create initial specifications only. May not approve its own output. Must work from user requirements and transform them into structured SDD-compliant specifications.

**Output location**: `specs/[feature-name]/spec.md`

### SpecRefinementAgent
May decompose, clarify, and restructure specifications. May not introduce new features or requirements beyond what the user explicitly requested. Focuses on removing ambiguity and ensuring completeness.

**Output location**: Modifies existing `specs/[feature-name]/spec.md`

### QualityReviewAgent
Acts as the primary constitutional enforcer. Can reject or request revisions to any specification. Cannot rewrite content, only evaluate against constitutional principles and SDD standards.

**Authority**: Block progression from Phase-1 to Phase-2 if specifications fail constitutional checks.

### CLISystemsAgent
Defines CLI interaction patterns only. Must not include implementation logic, algorithms, or code. Focuses on command structure, argument parsing, and help documentation.

**Constraint**: Output must be specification documents, not executable CLI applications.

### ImplementationPlannerAgent
May outline implementation roadmap and break down specifications into tasks. Must not include code, algorithms, or pseudo-code. Creates the bridge from specification to implementation preparation.

**Output location**: `specs/[feature-name]/plan.md` and `specs/[feature-name]/tasks.md`

### ProductArchitectAgent
Orchestrates agent execution and enforces phase boundaries. Has final authority on Phase-1 completion and specification approval. Ensures no Phase-2 work begins before Phase-1 artifacts are complete and reviewed.

**Responsibility**: Constitutional compliance verification and phase gate enforcement.

## Constraints

- **No application code** in Phase-1 (including prototypes, proofs-of-concept, or experimental implementations)
- **No pseudo-code** resembling real implementation logic
- **No configuration files** for runtime systems
- **No dependency installation** scripts or package manifests
- **No database schemas** or migration files (conceptual data models in documentation are permitted)
- **No executable artifacts** of any kind

**Rationale**: Phase-1 is exclusively for specification and design. Implementation activities belong in Phase-2 and beyond.

## Governance

This constitution governs all Phase-1 activities for Hackathon II – The Evolution of Todo. It is the highest authority during the specification phase and supersedes any conflicting practices or patterns.

### Amendment Process
1. Proposed amendments must be documented with clear rationale
2. All amendments require approval from ProductArchitectAgent
3. Amendments must include impact assessment on in-flight specifications
4. Version number must be incremented according to semantic versioning
5. Last amended date must be updated to reflect changes

### Compliance Review
Every specification must pass constitutional review before:
- Progressing to Phase-2 implementation
- Being marked as "approved" or "complete"
- Serving as basis for implementation planning

QualityReviewAgent is responsible for conducting compliance reviews and certifying constitutional adherence.

### Version Control
Changes to the constitution are tracked via version number and amendment dates. Breaking changes to core principles require major version increment. Additions or clarifications require minor version increment. Wording improvements require patch version increment.

**Version**: 1.0.0 | **Ratified**: 2026-01-27 | **Last Amended**: 2026-01-27
