import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Template:
    id: str
    category: str
    name: str
    body: str
    placeholders: list[str] = field(default_factory=list)


def _extract_placeholders(text: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"\[([^\[\]]+)\]", text)))


def parse_templates(repo_path: Path) -> dict[str, list[Template]]:
    md = (repo_path / "docs" / "templates.md").read_text(encoding="utf-8")
    result: dict[str, list[Template]] = {}
    current_category = ""
    current_name = ""
    in_text_block = False
    block_lines: list[str] = []
    template_index = 0

    for line in md.splitlines():
        # Category heading
        if line.startswith("### "):
            current_category = line[4:].strip()
            result.setdefault(current_category, [])
            continue

        # Template name label (bold, not 避坑指南)
        bold_match = re.match(r"^\*\*(.+?)\*\*$", line.strip())
        if bold_match and not in_text_block:
            current_name = bold_match.group(1)
            continue

        # Start of a text code block (skip json blocks)
        if line.strip() == "```text" and current_category:
            in_text_block = True
            block_lines = []
            continue

        # End of code block
        if line.strip() == "```" and in_text_block:
            in_text_block = False
            body = "\n".join(block_lines).strip()
            if body and current_category:
                template_index += 1
                tid = f"{template_index:03d}"
                placeholders = _extract_placeholders(body)
                result[current_category].append(
                    Template(
                        id=tid,
                        category=current_category,
                        name=current_name,
                        body=body,
                        placeholders=placeholders,
                    )
                )
            block_lines = []
            continue

        if in_text_block:
            block_lines.append(line)

    return {cat: templates for cat, templates in result.items() if templates}


def parse_gallery(repo_path: Path) -> dict[str, list[Template]]:
    result: dict[str, list[Template]] = {}
    example_index = 0

    _extra = Path(__file__).parent / "extra_gallery"
    _search = [
        *[(repo_path / "docs" / f) for f in ("gallery-part-1.md", "gallery-part-2.md")],
        *(sorted(_extra.glob("*.md")) if _extra.exists() else []),
    ]
    for path in _search:
        if not path.exists():
            continue
        md = path.read_text(encoding="utf-8")
        current_category = ""
        current_name = ""
        in_text_block = False
        block_lines: list[str] = []

        for line in md.splitlines():
            # Gallery example heading: ### 例 N：Category
            if line.startswith("### 例"):
                m = re.match(r"^### 例\s*\d+[：:]\s*(.+)$", line)
                if m:
                    current_category = m.group(1).strip()
                    current_name = line[4:].strip()
                    result.setdefault(current_category, [])
                continue

            if line.strip() == "```text" and current_category:
                in_text_block = True
                block_lines = []
                continue

            if line.strip() == "```" and in_text_block:
                in_text_block = False
                body = "\n".join(block_lines).strip()
                if body and current_category:
                    example_index += 1
                    result[current_category].append(
                        Template(
                            id=f"g{example_index:03d}",
                            category=current_category,
                            name=current_name,
                            body=body,
                            placeholders=[],  # gallery prompts are complete, no filling needed
                        )
                    )
                block_lines = []
                continue

            if in_text_block:
                block_lines.append(line)

    return {cat: items for cat, items in result.items() if items}
