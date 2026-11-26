# agentic-design-plugin

Autonomous UI/UX design and design-to-code companion plugin for [Google Antigravity](https://antigravity.google), powered by official **PenPot MCP** integration.

## Overview
`agentic-design-plugin` hosts the `@coding-design` subagent, enabling bidirectional UI/UX design workflows directly inside Antigravity sessions:
- **PenPot Authoring**: Create and update PenPot files, pages, artboards, frames, components, auto-layout structures, typography, and design tokens.
- **PenPot Inspection**: Inspect existing designs, extract layout hierarchies, spacing, color/typography tokens, and export design references.
- **Design Specification Synthesis**: Produce structured `<appDataDir>/brain/<conversation-id>/design-spec.md` artifacts for `@coding-develop`.

## Features
- **Declarative Subagent (`@coding-design`)**: Defined in [`agents/coding-design/agent.md`](agents/coding-design/agent.md) with `enable_mcp_tools: true` and strict read-only workspace source code boundaries (no `edit_file` or `run_command`).
- **Progressive Skill (`coding-design`)**: Workflow runbook in [`skills/coding-design/SKILL.md`](skills/coding-design/SKILL.md).
- **Dual-Mode Relay Protocols**: Supports both Standalone Mode (`ask_question` / `RequestFeedback=True`) and Subagent Mode (`[QUESTION_RELAY_REQUEST]` / `[ARTIFACT_APPROVAL_REQUEST]` via `send_message`) to prevent 60-second subagent timeouts.
- **Cross-Plugin Integration**:
  - Archives approved designs under `agentic-obsidian/designs/` via `@coding-document` when `agentic-project-documenting-plugin` is installed.
  - Supports optional handoff to `@coding` in Standalone Mode when `agentic-coding-plugin` is installed.

## PenPot MCP Configuration

PenPot MCP is configured externally in your Antigravity MCP configuration (rather than bundled in this repository) using a configurable HTTP/SSE endpoint:

```json
{
  "mcpServers": {
    "penpot": {
      "serverUrl": "${PENPOT_MCP_URL:-http://localhost:4401/mcp}"
    }
  }
}
```

### Environment Variables
- `PENPOT_MCP_URL` *(optional)*: Override the default PenPot MCP endpoint (`http://localhost:4401/mcp`).
- **Stdio (`npx`) Alternative**: If your local setup uses the stdio PenPot MCP package instead of HTTP/SSE, configure the `penpot` entry in your Antigravity MCP configuration with a `command`/`args` entry using `npx` (avoiding hardcoded machine-local paths).

## Installation & Activation

```bash
# Enable in Antigravity session:
agy plugin enable agentic-design-plugin
```

## Testing

Run the offline contract test suite via `uv`:

```bash
uv run pytest
```

## License
This project is licensed under the [MIT License](LICENSE).
