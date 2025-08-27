---
title: "Claude Code: Enable 1 Million Token Context (Sonnet 4) — Complete Guide 2025"
date: 2025-08-27
tags:
  - Claude Code
  - Sonnet 4
  - 1M token context
  - CLI tools
  - sub-agents
  - code automation
  - software development
  - AI coding assistant
categories:
  - Development Tools
  - AI for Developers
description: "Complete guide to setting up Claude Code with 1 million token context. Learn how to enable Sonnet 4 [1m], configure project memory via CLAUDE.md, and create sub-agents for automated testing, code review, and deployment."
keywords: "Claude Code, Sonnet 4, 1M token context, CLI, sub-agents, development automation, CLAUDE.md, code testing, code review, AI assistant"
summary: "Step-by-step guide to enable Sonnet 4 [1m] in CLI with 1 million token context, organize project memory (CLAUDE.md), and configure sub-agents for full-stack development automation."
---

# How to Enable 1 Million Token Context in Claude Code (Sonnet 4) — Complete Guide

> **Quick Start:**  
> 1) Run `claude`.  
> 2) Type `/model` and select **Sonnet 4 [1m]** (or specify manually: `/model sonnet[1m]`).  
> 3) Check active model: `/status`.  
> 4) Save "invariant" context in `CLAUDE.md`.  
> 5) Separate roles using **sub-agents** in `.claude/agents/`.  
> 6) Manage history: `/compact` (compress), `/clear` (start next stage with clean context).

---

## Table of Contents

- [1. Enabling 1M Context in CLI](#1-enabling-1m-context-in-cli)  
- [2. Project Memory: `CLAUDE.md` and Knowledge Import](#2-project-memory-claudemd-and-knowledge-import)  
- [3. Sub-agents: Context Isolation and Specialization](#3-sub-agents-context-isolation-and-specialization)  
- [4. Workflow Patterns: plan → code → test → review → docs → deploy](#4-workflow-patterns-plan--code--test--review--docs--deploy)  
- [5. History Management and Cost Control](#5-history-management-and-cost-control)  
- [6. Ready Files: `CLAUDE.md` and Sub-agents](#6-ready-files-claudemd-and-sub-agents)  
- [7. Quick Start (Script)](#7-quick-start-script)  
- [FAQ and Resources](#faq-and-resources)

---

## 1. Enabling 1 Million Token Context in Claude Code CLI

Claude Code with **Sonnet 4 [1m]** model provides unprecedented 1 million token context for working with large codebases. This is a revolutionary solution for full-stack developers seeking enhanced AI-powered development workflows.

**Step-by-step setup:**

1. **Launch Claude Code Interactive REPL:**
   ```bash
   claude
   ```

2. **Switch to 1M Context Model:**
   ```text
   /model
   ```
   Select **Sonnet 4 [1m]** from the menu. If the option isn't available in the menu, use direct command:
   ```text
   /model sonnet[1m]
   ```

3. **Verify Active Model:**
   ```text
   /status
   ```
   Ensure the output shows active Sonnet 4 model with 1M token support.

---

## 2. Project Memory: `CLAUDE.md` and Knowledge Import

To **preserve context between sessions** (architecture, code style rules, build/test commands, documentation links), create a `CLAUDE.md` file in the repository root. Its content is **automatically loaded** when starting Claude Code and supplements the system context. Store only **invariant** content (what's useful throughout the entire project).

> Where to store memory: globally — `~/.claude/CLAUDE.md`, project level — `./CLAUDE.md`. Can be combined (global preferences + project specifics).

---

## 3. Sub-agents: Context Isolation and Specialization

**Sub-agents** are specialized "mini-assistants" with **their own system prompt, tool set, and separate context window** that the main Claude agent can call proactively (by description) or on explicit command. They help **avoid "cluttering" main history** with lengthy test logs, reviews, etc., and make pipelines more reproducible. Stored in:  
- project: `.claude/agents/*.md`  
- user: `~/.claude/agents/*.md`  
Format — Markdown with YAML header.

---

## 4. Workflow Patterns: plan → code → test → review → docs → deploy

Example dialogue (after enabling `[1m]`):

```text
Create a feature plan based on docs/architecture.md and docs/openapi.yaml.
Split into MVP / Next. Format as checklists.

Let's start with MVP/Step 1 — implement backend endpoint per specification.
After changes:
- call test-runner sub-agent to run tests and fixes until green,
- then code-reviewer for change review,
- and doc-writer — update README/API section.

Finally ask deploy-manager — prepare Docker and GitHub Actions workflow.
```

> Tip: if file(s) are already in repository, just specify their paths (model will read them itself). If needed — allow `Read/Edit/Bash` (see `/config`/CLI flags).

---

## 5. History Management and Cost Control

- **Compress history** before new stage, preserving summary:  
  ```text
  /compact Summarize decisions and remaining tasks briefly
  ```
- **Clear context** for next stage:  
  ```text
  /clear
  ```
- **View available slash commands** and use them appropriately.

---

## 6. Ready Files: `CLAUDE.md` and Sub-agents

> Copy as-is, then adjust commands for your project.

### 6.1 `CLAUDE.md` (project memory)

```markdown
# Project: MyAIApp

## Architecture and Artifacts
- Architecture: docs/architecture.md
- API Contracts: docs/openapi.yaml
- Runbook: docs/runbook.md
- Decisions and Status: STATUS.md (maintain brief stage summaries)
- Work Plan: PLAN.md (MVP/Next, checklists)

## Technology Stack
- Backend: Python (pytest) / Go (go test) / Rust (cargo test)
- Frontend: TypeScript + React (vitest/jest)
- Containerization: Docker
- CI/CD: GitHub Actions

## Default Commands (adjust for your project)
### Python
- Install: `pip install -r requirements.txt`
- Tests: `pytest -q`
- Lint: `ruff check .` or `flake8`

### Go
- Tests: `go test ./...`
- Lint: `golangci-lint run`

### Rust
- Tests: `cargo test`
- Lint: `cargo clippy -- -D warnings`

### TypeScript / React
- Install: `pnpm i` or `npm ci`
- Tests: `pnpm test` or `npm test`
- Lint: `pnpm lint` or `npm run lint`
- Build: `pnpm build` or `npm run build`

### Docker
- Build: `docker build -t myapp:local .`
- Local run: `docker compose up --build`

### GitHub Actions
- Main workflow: `.github/workflows/ci.yml`
- Requirement: unit tests on PR and static analysis

## Code Policy
- Style: 2 space indent, self-documenting names, no default export
- Security: secrets only via env/secret manager, no hard-coding
- Test criteria: P0 scenarios must have unit tests

## Self-help During Work
- Always start with PLAN (checklist in PLAN.md).
- After stage completion: update STATUS.md and do `/compact`, then `/clear`.
```

---

### 6.2 `.claude/agents/test-runner.md`

```markdown
---
name: test-runner
description: Use proactively to run tests and fix failures.
# tools: (inherits default permissions: Read/Edit/Bash etc.)
---

You are a test automation engineer.
Task:
1) Automatically determine appropriate test command by project stack:
   - Python: `pytest -q`
   - Go: `go test ./...`
   - Rust: `cargo test`
   - TypeScript/React: `pnpm test` or `npm test`
2) Run tests. On failures:
   - Analyze stacktraces/logs.
   - Suggest minimal fixes preserving intent.
   - Apply code changes, re-run tests.
3) Repeat until **green tests** or clear blocker.
Response format:
- Result: ✅ all tests passed / ❌ failures exist
- What was fixed (file/fragment, briefly why)
- What remains and why (if blocker)
```

---

### 6.3 `.claude/agents/code-reviewer.md`

```markdown
---
name: code-reviewer
description: Expert code review. Proactively review after code changes.
tools: Read, Grep, Glob, Bash
---

You are an experienced code reviewer (quality/security/maintainability).
Actions:
1) Extract diff of recent changes (`git diff`), focus on changed files.
2) Check:
   - Security: injections, secrets, deserialization, access.
   - Quality: complexity, duplication, edge cases, error handling.
   - Style: compliance with CLAUDE.md rules.
3) Give clear recommendations with fix examples (before/after).
Format:
- Critical / Important / Suggestion — as lists
- Quick fixes (if trivial) — suggest patches
```

---

### 6.4 `.claude/agents/doc-writer.md`

```markdown
---
name: doc-writer
description: Technical documentation writer after significant changes.
tools: Read, Write
---

You are a technical writer. After substantial changes:
1) Update README.md (purpose, startup, examples).
2) Update API section (if affected), sync with docs/openapi.yaml.
3) Briefly describe changes in CHANGELOG.md.
Format:
- What was added/changed (1-3 paragraphs)
- How to run/test
```

---

### 6.5 `.claude/agents/deploy-manager.md`

```markdown
---
name: deploy-manager
description: Deployment & CI/CD specialist for release preparation.
tools: Bash
---

You are a DevOps engineer.
Steps:
1) Assess if DB migrations/environment variables/Dockerfile updates are needed.
2) Prepare:
   - Dockerfile / docker-compose.yml (if missing or outdated)
   - GitHub Actions workflow `.github/workflows/ci.yml`:
     - steps: checkout, setup (lang), install deps, lint, test, build, (optional) docker build/push
3) Output **deployment instructions** (locally and/or to chosen environment).
4) Don't execute destructive commands; ask confirmation for pushes/releases.
```

---

## 7. Quick Start (Script)

```bash
# 1) Project memory
cat > CLAUDE.md <<'EOF'
# Project: MyAIApp
... (insert content from section 6.1 above) ...
EOF

# 2) Sub-agents
mkdir -p .claude/agents

cat > .claude/agents/test-runner.md <<'EOF'
... (insert content 6.2) ...
EOF

cat > .claude/agents/code-reviewer.md <<'EOF'
... (insert content 6.3) ...
EOF

cat > .claude/agents/doc-writer.md <<'EOF'
... (insert content 6.4) ...
EOF

cat > .claude/agents/deploy-manager.md <<'EOF'
... (insert content 6.5) ...
EOF

echo "Ready. Run: claude → /model sonnet[1m] → /status"
```

---

## FAQ and Resources

- How to change model in Claude Code? — `/model`, current — `/status`.
- Where is documentation on memory (`CLAUDE.md`)? — Manage Memory section in docs.
- How do sub-agents work and where to store their files? — Subagents section.
- What slash commands are available for context? — `/compact` (compress history), `/clear` (reset history).
- Where to check CLI flags (model, tools)? — CLI reference.

---

## Video Tutorial

Watch a detailed video tutorial on setting up Claude Code with 1 million token context:

{{< youtube "-tvqEL-YFTI" >}}