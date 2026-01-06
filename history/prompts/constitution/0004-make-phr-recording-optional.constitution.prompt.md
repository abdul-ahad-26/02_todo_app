---
id: "0004"
title: "make-phr-recording-optional"
stage: "constitution"
date: "2026-01-06"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "none"
branch: "main"
user: "human"
command: "/sp.constitution don't record prompt history on every message."
labels: [constitution,phr,governance]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - ".specify/memory/constitution.md"
  - ".claude/commands/sp.constitution.md"
tests: []
---

## Prompt

don't record prompt history on every message.

## Response snapshot

Updated constitution from v1.2.0 to v1.3.0:
- Changed Section I.3 from MUST to SHOULD for PHR creation
- Removed "PHR for Every Input" row from Enforcement Rules table
- Updated sp.constitution.md command file to reflect optional PHR guidance

## Outcome

- ✅ Impact: PHR recording is now optional (SHOULD) rather than mandatory (MUST)
- 🧪 Tests: None required (constitution amendment only)
- 📁 Files: 2 files modified
- 🔁 Next prompts: None
- 🧠 Reflection: Minor governance update to reduce overhead for routine interactions

## Evaluation notes (flywheel)

- Failure modes observed: "null"
- Graders run and results (PASS/FAIL): "null"
- Prompt variant (if applicable): "null"
- Next experiment (smallest change to try): "null"
