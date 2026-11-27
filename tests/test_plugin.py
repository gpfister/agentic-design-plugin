"""Offline contract tests for agentic-design-plugin structure and specifications."""

import json
import re
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent


def _extract_frontmatter(content: str) -> str:
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    assert match is not None, "Expected YAML frontmatter delimited by ---"
    return match.group(1)


def test_plugin_manifest_valid():
    manifest_file = PLUGIN_ROOT / "plugin.json"
    assert manifest_file.exists(), "plugin.json must exist"
    data = json.loads(manifest_file.read_text(encoding="utf-8"))
    assert data.get("name") == "agentic-design-plugin"
    assert data.get("version") == "0.1.0"
    assert data.get("license") == "MIT"
    assert isinstance(data.get("description"), str) and len(data["description"]) > 0


def test_mcp_config_not_bundled():
    mcp_file = PLUGIN_ROOT / "mcp_config.json"
    assert not mcp_file.exists(), "mcp_config.json must not be bundled in the repository"


def test_pyproject_valid():
    pyproject_file = PLUGIN_ROOT / "pyproject.toml"
    assert pyproject_file.exists(), "pyproject.toml must exist"
    content = pyproject_file.read_text(encoding="utf-8")
    assert 'name = "agentic-design-plugin"' in content
    assert 'version = "0.1.0"' in content
    assert 'requires-python = ">=3.11"' in content
    assert "pydantic>=2.10.0" in content
    assert "pytest>=8.0.0" in content


def test_license_and_readme_exist():
    license_file = PLUGIN_ROOT / "LICENSE"
    assert license_file.exists(), "LICENSE must exist"
    license_text = license_file.read_text(encoding="utf-8")
    assert "MIT License" in license_text
    assert "Greg PFISTER" in license_text

    readme_file = PLUGIN_ROOT / "README.md"
    assert readme_file.exists(), "README.md must exist"
    readme_text = readme_file.read_text(encoding="utf-8")
    assert "agentic-design-plugin" in readme_text
    assert "@coding-design" in readme_text
    assert "PENPOT_MCP_URL" in readme_text
    assert "design-spec.md" in readme_text
    assert "/Users/" not in readme_text


def test_rules_agents_md_contract():
    rules_file = PLUGIN_ROOT / "rules" / "AGENTS.md"
    assert rules_file.exists(), "rules/AGENTS.md must exist"
    content = rules_file.read_text(encoding="utf-8")
    assert "@coding-develop" in content
    assert "edit_file" in content
    assert "design-spec.md" in content
    assert "[QUESTION_RELAY_REQUEST]" in content
    assert "[ARTIFACT_APPROVAL_REQUEST]" in content
    assert "agentic-obsidian/designs/" in content
    assert "@coding-document" in content
    assert "@coding" in content
    assert "coding-clarify" in content
    assert "coding-specify" in content
    assert "## Design Resources" in content
    assert "semantic version" in content.lower()
    assert "DESIGN.md" in content
    assert "assets/" in content
    assert "docs/design/" in content
    assert "component reuse" in content.lower()


def test_coding_design_agent_definition():
    agent_file = PLUGIN_ROOT / "agents" / "coding-design" / "agent.md"
    assert agent_file.exists(), "agents/coding-design/agent.md must exist"
    content = agent_file.read_text(encoding="utf-8")
    fm = _extract_frontmatter(content)

    assert "name: coding-design" in fm
    assert "enable_write_tools: true" in fm
    assert "enable_subagent_tools: true" in fm
    assert "enable_mcp_tools: true" in fm

    tools_match = re.search(r"tools:\s*\n((?:\s*-\s+[^\n]+\n?)+)", fm)
    assert tools_match is not None, "tools list must be present in frontmatter"
    declared_tools = [
        line.strip().lstrip("-").strip()
        for line in tools_match.group(1).strip().splitlines()
    ]
    expected_tools = {
        "read_file",
        "list_dir",
        "write_file",
        "send_message",
        "ask_question",
        "invoke_subagent",
    }
    assert set(declared_tools) == expected_tools
    assert "edit_file" not in declared_tools
    assert "run_command" not in declared_tools

    assert "design-spec.md" in content
    assert "[QUESTION_RELAY_REQUEST]" in content
    assert "[ARTIFACT_APPROVAL_REQUEST]" in content
    assert "coding-clarify" in content
    assert "coding-specify" in content
    assert "## Design Resources" in content
    assert "semantic version" in content.lower()
    assert "Component Reuse Audit" in content
    assert "Local Repository Resource Sync" in content
    assert "DESIGN.md" in content
    assert "assets/" in content
    assert "docs/design/" in content


def test_coding_design_skill_definition():
    skill_file = PLUGIN_ROOT / "skills" / "coding-design" / "SKILL.md"
    assert skill_file.exists(), "skills/coding-design/SKILL.md must exist"
    content = skill_file.read_text(encoding="utf-8")
    fm = _extract_frontmatter(content)

    assert "name: coding-design" in fm
    assert "description:" in fm
    assert "PenPot" in content
    assert "design-spec.md" in content
    assert "[QUESTION_RELAY_REQUEST]" in content
    assert "[ARTIFACT_APPROVAL_REQUEST]" in content
    assert "coding-clarify" in content
    assert "coding-specify" in content
    assert "## Design Resources" in content
    assert "semantic version" in content.lower()
    assert "Component Reuse Audit" in content
    assert "Local Repository Resource Sync" in content
    assert "DESIGN.md" in content
    assert "assets/" in content
    assert "docs/design/" in content
    assert "component reuse" in content.lower()
    assert "PENPOT_MCP_URL" in content
