# AGENTS.md — xingtu-learn

## Purpose and scope
Read `README.md` and the files relevant to the requested change. This repository has its own source-of-truth rules; do not import instructions from another repository implicitly.

## Local guardrails
This repository publishes reusable learning processes. Separate verified facts, personal reflections, hypotheses and sources. Never publish private notes or unapproved personal details. Keep learning tracks and linked deliverables internally consistent.

## Shared Agent assets
- Shared reusable Skills: https://github.com/xingtu1996/xingtu-skills
- SDD method and validator: https://github.com/xingtu1996/xingtu-sdd
- Shared rules and hooks: xingtu-rules and xingtu-hooks.
- Cross-repository references are **not** automatic inheritance. Explicitly verify installation, supported scope and versions before use.

## Delivery workflow
1. Inspect existing instructions and source files; check for more specific directory-level guidance.
2. Use a small, reviewable SDD spec for meaningful behavior changes and define acceptance evidence first.
3. Make changes on a dedicated branch and open a Draft PR. Do not merge or publish automatically.
4. Run relevant checks only in a safe environment. Report the exact commands, CI links and outcomes; mark anything unrun as NOT_RUN.
5. Protect secrets, private Vault content and personal information. Preserve licenses and maintain a rollback path.
