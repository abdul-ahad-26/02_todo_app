---
id: "0003"
title: "Mandate phase based top level folders in constitution"
stage: "constitution"
date: "2026-01-01"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "none"
branch: "002-web-todo"
user: "default"
command: "user observation"
labels: ["constitution", "structure", "phases"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - ".specify/memory/constitution.md"
tests:
  - "manual verification of directory naming convention"
---

## Prompt

do the constitution specify that each phase should have a dedicated folder. e.g. for phase 2 /phase-2-web/ and phase 3 /phase-3-.. .

## Response snapshot

I have updated the Constitution to explicitly mandate a phase-based project structure. Each phase must now be contained in its own dedicated top-level directory (e.g., `phase-1-console/`, `phase-2-web/`) to preserve the historical evolution of the project.

## Outcome

- ✅ Impact: High - Standardizes repo structure for multi-phase evolution.
- 🧪 Tests: N/A (Documentation change).
- 📁 Files: Updated .specify/memory/constitution.md to v1.2.0.
- 🔁 Next prompts: Use mandated naming conventions for subsequent phases.
- 🧠 Reflection: Explicitly defining directory structure in the constitution prevents fragmented repo layouts as the project scales.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
