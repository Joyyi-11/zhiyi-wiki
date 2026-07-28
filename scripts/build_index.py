from dataclasses import dataclass
from pathlib import Path
import sys

import frontmatter
import yaml


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = PROJECT_ROOT / "INDEX.md"
KNOWLEDGE_ROLE_LABELS = {
    "personal_basis": "个人基准",
    "curated_influence": "重要认知来源",
    "external_input": "外部输入",
}


@dataclass(frozen=True)
class IndexItem:
    path: Path
    title: str
    metadata: dict[str, object]


def load_items(directory: Path) -> list[IndexItem]:
    if not directory.is_dir():
        raise FileNotFoundError(f"Directory not found: {directory}")

    items = []
    for path in directory.glob("*.md"):
        with path.open(encoding="utf-8-sig") as markdown_file:
            document = frontmatter.load(markdown_file)

        title = document.metadata.get("title")
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"{path.name}: missing a non-empty title")

        items.append(
            IndexItem(
                path=path,
                title=title.strip(),
                metadata=document.metadata,
            )
        )

    return items


def read_string_list(item: IndexItem, field: str) -> list[str]:
    value = item.metadata.get(field, [])
    if not isinstance(value, list) or not all(isinstance(entry, str) for entry in value):
        raise ValueError(f"{item.path.name}: {field} must be a list of strings")
    return value


def markdown_link(item: IndexItem, project_root: Path) -> str:
    relative_path = item.path.relative_to(project_root).as_posix()
    target = f"<{relative_path}>" if " " in relative_path else relative_path
    return f"[{item.title}]({target})"


def format_tags(item: IndexItem) -> str:
    tags = read_string_list(item, "tags")
    return "、".join(tags) if tags else "无"


def read_knowledge_role(item: IndexItem) -> str:
    role = item.metadata.get("knowledge_role")
    if role not in KNOWLEDGE_ROLE_LABELS:
        allowed = ", ".join(KNOWLEDGE_ROLE_LABELS)
        raise ValueError(
            f"{item.path.name}: knowledge_role must be one of: {allowed}"
        )
    return role


def render_index(project_root: Path) -> tuple[str, dict[str, int]]:
    topics = sorted(
        load_items(project_root / "wiki" / "topics"),
        key=lambda item: item.title.casefold(),
    )
    entities = sorted(
        load_items(project_root / "wiki" / "entities"),
        key=lambda item: item.title.casefold(),
    )
    notes = sorted(
        load_items(project_root / "notes"),
        key=lambda item: item.path.name.casefold(),
        reverse=True,
    )

    lines = [
        "# 知识库索引",
        "",
        "> 此文件由 `python scripts/build_index.py` 自动生成，请勿手工编辑。",
        "",
        f"## 主题页（{len(topics)}）",
        "",
    ]

    if topics:
        for item in topics:
            status = item.metadata.get("status", "unknown")
            lines.append(
                f"- {markdown_link(item, project_root)} · 状态：{status} · 标签：{format_tags(item)}"
            )
    else:
        lines.append("- 暂无")

    lines.extend(["", f"## 实体页（{len(entities)}）", ""])
    if entities:
        for item in entities:
            entity_type = item.metadata.get("entity_type", "unknown")
            lines.append(
                f"- {markdown_link(item, project_root)} · 类型：{entity_type}"
            )
    else:
        lines.append("- 暂无")

    notes_by_role = {role: [] for role in KNOWLEDGE_ROLE_LABELS}
    for item in notes:
        notes_by_role[read_knowledge_role(item)].append(item)

    lines.extend(["", f"## 单源笔记（{len(notes)}）", ""])
    for role, label in KNOWLEDGE_ROLE_LABELS.items():
        role_notes = notes_by_role[role]
        lines.extend([f"### {label}（{len(role_notes)}）", ""])
        if role_notes:
            for item in role_notes:
                date = item.metadata.get("date", "未知日期")
                lines.append(
                    f"- {markdown_link(item, project_root)} · 日期：{date} · 标签：{format_tags(item)}"
                )
        else:
            lines.append("- 暂无")
        lines.append("")

    counts = {
        "topics": len(topics),
        "entities": len(entities),
        "notes": len(notes),
    }
    return "\n".join(lines).rstrip() + "\n", counts


def build_index(project_root: Path = PROJECT_ROOT) -> tuple[bool, dict[str, int]]:
    rendered, counts = render_index(project_root)
    index_path = project_root / "INDEX.md"
    content = chr(0xFEFF) + rendered

    if index_path.exists() and index_path.read_text(encoding="utf-8") == content:
        return False, counts

    index_path.write_text(content, encoding="utf-8", newline="\n")
    return True, counts


def main() -> int:
    try:
        updated, counts = build_index()
    except (OSError, UnicodeError, ValueError, TypeError, yaml.YAMLError) as error:
        print(f"Failed to build index: {error}", file=sys.stderr)
        return 1

    status = "updated" if updated else "unchanged"
    print(
        f"Index {status}: {counts['topics']} topics, "
        f"{counts['entities']} entities, {counts['notes']} notes."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
