# UI/UX Design & PenPot Standards — agentic-design-plugin

This rule set applies whenever the `agentic-design-plugin` is active in an Antigravity session.

---

## 1. Design Principles & Workspace Safety
- **Exclusive `@coding-develop` Code-Change Authority**: `@coding-design` MUST remain strictly read-only with respect to workspace source code, configuration files, and test suites.
  - `edit_file` is strictly prohibited and MUST NOT be declared or used.
  - `run_command` is omitted and MUST NOT be used to mutate repository state.
  - `write_file` is restricted exclusively to the session artifact `<appDataDir>/brain/<conversation-id>/design-spec.md`.
  - Repository source code, UI components, CSS/design tokens, and tests MUST only be modified by `@coding-develop` under `@coding` orchestration.
- **Bidirectional PenPot MCP Scope**: Authoring and mutation are permitted **only** inside PenPot design files via official PenPot MCP tools (files, pages, artboards, frames, components, auto-layout, typography, color palettes, and design tokens).
- **Non-Destructive Semantic Versioning (PenPot Pages & Screens)**:
  - Prefix or suffix PenPot pages and screens with semantic version identifiers (e.g., `v1.0 - <PageName>` or `<PageName> (v2)`).
  - Never overwrite or delete prior versioned pages or screens unless explicitly instructed; before editing any existing versioned page or screen, duplicate the previous versioned page/screen in PenPot so prior versions remain preserved as read-only history.
- **Component Reuse Enforcement**: Before authoring new UI elements in PenPot, inspect existing PenPot component libraries and codebase UI components (`read_file`, `list_dir`). Reuse existing components and design tokens wherever possible and define reusable PenPot components and explicit component hierarchies in `design-spec.md`.
- **Local Repository Resource Sync Targets**: While `@coding-design` remains strictly read-only on workspace files, `design-spec.md` MUST explicitly declare all required local repository sync targets—`DESIGN.md`, `assets/`, and `docs/design/<resource>.penpot`—alongside exported SVG/PNG/design tokens so `@coding-plan` can schedule them and `@coding-develop` can write and commit them in `.worktrees/<slug>`.
- **Fail-Fast MCP Connectivity**: If the PenPot MCP server is unreachable or returns connection/tool errors, report the exact endpoint configuration error (`PENPOT_MCP_URL` / `mcp_config.json`) with setup guidance from `README.md` and halt immediately without fabricating design data.

---

## 2. Interactive Clarification & Approval Gates
- **One Question at a Time**: When clarifying UI/UX requirements, layout constraints, or design-token conventions, ask strictly **one question at a time**.
- **Dual-Mode Question Relay Protocol**:
  - **Subagent Mode (Caller ID Present)**: Do NOT call `ask_question` directly. Relay questions via `send_message` using `[QUESTION_RELAY_REQUEST]` and await `[QUESTION_RELAY_RESPONSE]` before proceeding.
  - **Standalone Mode (Root Agent)**: Call `ask_question` directly at the session root.
- **Dual-Mode Artifact Approval Relay Protocol (`design-spec.md`)**:
  - **Subagent Mode (Caller ID Present)**: Do NOT call `write_file` with `RequestFeedback=True` (to prevent the 60-second background subagent execution timeout). Write `design-spec.md` directly to disk, dispatch `[ARTIFACT_APPROVAL_REQUEST]` to `caller_id` via `send_message`, and enter IDLE state awaiting `[ARTIFACT_APPROVAL_RESPONSE]`.
  - **Standalone Mode (Root Agent)**: Write `design-spec.md` with `ArtifactMetadata={"RequestFeedback": True, "UserFacing": True, "Summary": ...}` as the **sole and final tool call** of that turn so Antigravity renders Approve / Reject buttons.

---

## 3. Cross-Plugin Integration & Handoffs
- **Early Discovery / Creation Mode (`coding-clarify` / `coding-specify`)**:
  - For UI applications, `@coding` may invoke `@coding-design` during `coding-clarify` or `coding-specify` *before* `specification.md` is finalized.
  - In early discovery/creation mode, `@coding-design` inspects existing workspace design artifacts (`DESIGN.md`, `docs/design/*.penpot`, `assets/`), locates existing or initializes new PenPot files/pages/screens (following non-destructive semantic versioning), and returns PenPot file/page/versioned screen IDs and links to populate `specification.md` `## Design Resources`.
- **Obsidian Vault Archival (`@coding-document`)**:
  - When `agentic-project-documenting-plugin` is installed, `@coding-design` MUST invoke `@coding-document` upon `design-spec.md` approval to archive design specifications, PenPot links, and design-token references under `agentic-obsidian/designs/`.
  - When `agentic-project-documenting-plugin` is not installed, retain `design-spec.md` as the local session artifact without failing.
- **Optional Implementation Handoff (`@coding` in Standalone Mode)**:
  - Upon approval of `design-spec.md` in Standalone Mode, if `agentic-coding-plugin` is installed, ask the user whether to invoke `@coding` to implement the UI changes using the standardized orchestration prompt:
    ```text
    Orchestrate the 7-stage software development lifecycle to implement the following feature / correction based on the approved assessment: <path-to-design-spec.md>. Do not implement directly; delegate all phases through worker subagents.
    ```
  - If `agentic-coding-plugin` is not installed, present `design-spec.md` directly without invoking `@coding`.

---

## 4. Communication & Links
- Keep design summaries structured, concise, and high-signal.
- Always generate clickable markdown links using the `file://` scheme when referencing workspace files or `design-spec.md`.
- Use GitHub Flavored Markdown alerts (`> [!NOTE]`, `> [!IMPORTANT]`, `> [!TIP]`, `> [!WARNING]`) appropriately without nesting.
