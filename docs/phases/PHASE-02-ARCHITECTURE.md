# Phase 02 — Architecture & Repository Structure

## Read
- assignment architecture section
- PRD
- FRs
- NFRs
- use cases
- repository layout requirement
- DevOps/K8s/CI-CD sections

## Tasks
1. Reconstruct the exact assignment repository layout.
2. Compare it to current repo.
3. Resolve deviations through documented migration steps.
4. Create architecture docs and Mermaid diagrams.
5. Define layer boundaries and dependency direction.
6. Define network boundaries.
7. Define data flows.
8. Define operational dependencies.
9. Create ADRs for non-obvious architectural choices.

## Special
The assignment's frontend must not own business rules.
Backend must use routes → services → repositories/providers.
Frontend must not reach the database.

## Gate
Architecture is complete enough that implementation tickets can be created without guessing.
