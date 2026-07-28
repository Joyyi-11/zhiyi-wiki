from pathlib import Path
import sys

import frontmatter
import yaml

from build_index import render_index


PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTE_LIST_FIELDS = ("tags", "entities")
KNOWLEDGE_ROLES = {"personal_basis", "curated_influence", "external_input"}
REQUIRED_TOPIC_SECTIONS = (
    "当前结论",
    "边界与矛盾",
    "挑战视角",
    "待验证问题",
    "来源",
)


def load_document(path: Path, errors: list[str]):
    try:
        with path.open(encoding="utf-8-sig") as markdown_file:
            return frontmatter.load(markdown_file)
    except (OSError, UnicodeError, TypeError, yaml.YAMLError) as error:
        errors.append(f"{path}: cannot parse frontmatter: {error}")
        return None


def read_string_list(
    metadata: dict[str, object],
    field: str,
    path: Path,
    errors: list[str],
) -> list[str]:
    value = metadata.get(field)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        errors.append(f"{path}: {field} must be a list of strings")
        return []
    return value


def validate_repository(project_root: Path = PROJECT_ROOT) -> list[str]:
    errors: list[str] = []
    notes_dir = project_root / "notes"
    topics_dir = project_root / "wiki" / "topics"
    entities_dir = project_root / "wiki" / "entities"
    briefs_dir = project_root / "briefs"

    for directory in (notes_dir, topics_dir, entities_dir, briefs_dir):
        if not directory.is_dir():
            errors.append(f"{directory}: directory not found")

    if notes_dir.is_dir():
        for path in sorted(notes_dir.glob("*.md")):
            document = load_document(path, errors)
            if document is None:
                continue
            metadata = document.metadata

            for field in ("title", "source_type"):
                value = metadata.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{path}: {field} must be a non-empty string")
            knowledge_role = metadata.get("knowledge_role")
            if knowledge_role not in KNOWLEDGE_ROLES:
                allowed = ", ".join(sorted(KNOWLEDGE_ROLES))
                errors.append(
                    f"{path}: knowledge_role must be one of: {allowed}"
                )
            if "date" not in metadata:
                errors.append(f"{path}: date is required")
            for field in NOTE_LIST_FIELDS:
                read_string_list(metadata, field, path, errors)

            source_path = metadata.get("source_path")
            if metadata.get("source_type") == "own_thought":
                # 想法没有外部原料，source_path 可空；非空时仍需指向真实文件
                if isinstance(source_path, str) and source_path.strip():
                    if not (path.parent / source_path).resolve().is_file():
                        errors.append(f"{path}: source_path does not exist: {source_path}")
            elif not isinstance(source_path, str) or not source_path.strip():
                errors.append(f"{path}: source_path must be a non-empty string")
            elif not (path.parent / source_path).resolve().is_file():
                errors.append(f"{path}: source_path does not exist: {source_path}")

            source_url = metadata.get("source_url")
            if source_url is not None and (
                not isinstance(source_url, str) or not source_url.strip()
            ):
                errors.append(f"{path}: source_url must be a non-empty string")

    for directory, expected_type in ((topics_dir, "topic"), (entities_dir, "entity")):
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.md")):
            document = load_document(path, errors)
            if document is None:
                continue
            metadata = document.metadata
            if metadata.get("type") != expected_type:
                errors.append(f"{path}: type must be {expected_type}")
            title = metadata.get("title")
            if not isinstance(title, str) or not title.strip():
                errors.append(f"{path}: title must be a non-empty string")
            for source in read_string_list(metadata, "sources", path, errors):
                if not (path.parent / source).resolve().is_file():
                    errors.append(f"{path}: source does not exist: {source}")
            if expected_type == "entity" and "topics" in metadata:
                for topic in read_string_list(metadata, "topics", path, errors):
                    if not (path.parent / topic).resolve().is_file():
                        errors.append(f"{path}: topic does not exist: {topic}")
            if expected_type == "topic":
                body = document.content or ""
                for section in REQUIRED_TOPIC_SECTIONS:
                    if section not in body:
                        errors.append(
                            f"{path}: missing required section '{section}'"
                        )

    if briefs_dir.is_dir():
        for path in sorted(briefs_dir.glob("*.md")):
            document = load_document(path, errors)
            if document is None:
                continue
            if document.metadata.get("type") != "brief":
                errors.append(f"{path}: type must be brief")
            for field in ("source_topics", "source_notes"):
                for source in read_string_list(document.metadata, field, path, errors):
                    if not (path.parent / source).resolve().is_file():
                        errors.append(f"{path}: {field} target does not exist: {source}")

    index_path = project_root / "INDEX.md"
    try:
        rendered, _ = render_index(project_root)
        expected_index = chr(0xFEFF) + rendered
        if not index_path.is_file():
            errors.append(f"{index_path}: file not found")
        elif index_path.read_text(encoding="utf-8") != expected_index:
            errors.append(f"{index_path}: index is stale")
    except (OSError, UnicodeError, ValueError, TypeError, yaml.YAMLError) as error:
        errors.append(f"{index_path}: cannot render index: {error}")

    return errors


def main() -> int:
    errors = validate_repository()
    if errors:
        print(f"Validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
