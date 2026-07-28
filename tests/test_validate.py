import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import frontmatter


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from build_index import build_index  # noqa: E402
from validate import validate_repository  # noqa: E402


class ValidateRepositoryTests(unittest.TestCase):
    def test_current_repository_is_valid(self) -> None:
        self.assertEqual(validate_repository(PROJECT_ROOT), [])

    def test_missing_local_source_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            project_root = Path(directory)
            notes_dir = project_root / "notes"
            notes_dir.mkdir()
            (project_root / "wiki" / "topics").mkdir(parents=True)
            (project_root / "wiki" / "entities").mkdir(parents=True)
            (project_root / "briefs").mkdir()

            self.write_note(notes_dir / "note.md")
            build_index(project_root)

            errors = validate_repository(project_root)

            self.assertTrue(
                any("source_path does not exist" in error for error in errors)
            )

    def test_invalid_knowledge_role_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            project_root = Path(directory)
            notes_dir = project_root / "notes"
            raw_dir = project_root / "raw"
            notes_dir.mkdir()
            raw_dir.mkdir()
            (project_root / "wiki" / "topics").mkdir(parents=True)
            (project_root / "wiki" / "entities").mkdir(parents=True)
            (project_root / "briefs").mkdir()
            (raw_dir / "source.md").write_text("source", encoding="utf-8")

            note = frontmatter.Post(
                "# Body\n",
                title="Invalid role",
                date="2026-07-19",
                source_type="web",
                source_path="../raw/source.md",
                knowledge_role="unknown",
                tags=[],
                entities=[],
            )
            path = notes_dir / "note.md"
            path.write_text(frontmatter.dumps(note), encoding="utf-8")

            errors = validate_repository(project_root)

            self.assertTrue(any("knowledge_role must be one of" in error for error in errors))

    def test_topic_missing_challenge_section_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            project_root = Path(directory)
            notes_dir = project_root / "notes"
            raw_dir = project_root / "raw"
            topics_dir = project_root / "wiki" / "topics"
            notes_dir.mkdir()
            raw_dir.mkdir()
            topics_dir.mkdir(parents=True)
            (project_root / "wiki" / "entities").mkdir(parents=True)
            (project_root / "briefs").mkdir()
            (raw_dir / "source.md").write_text("source", encoding="utf-8")

            note = frontmatter.Post(
                "# Body\n",
                title="Source note",
                date="2026-07-19",
                source_type="web",
                source_path="../raw/source.md",
                knowledge_role="external_input",
                tags=[],
                entities=[],
            )
            (notes_dir / "note.md").write_text(frontmatter.dumps(note), encoding="utf-8")

            topic = frontmatter.Post(
                "# 当前结论\n\n结论。\n\n## 边界与矛盾\n\n矛盾。\n\n## 待验证问题\n\n问题。\n\n## 来源\n\n- [note](../../notes/note.md)\n",
                title="Incomplete topic",
                type="topic",
                status="developing",
                tags=["示例"],
                sources=["../../notes/note.md"],
            )
            (topics_dir / "topic.md").write_text(frontmatter.dumps(topic), encoding="utf-8")

            errors = validate_repository(project_root)

            self.assertTrue(
                any("missing required section '挑战视角'" in error for error in errors)
            )

    def test_own_thought_without_source_path_is_accepted(self) -> None:
        with TemporaryDirectory() as directory:
            project_root = Path(directory)
            notes_dir = project_root / "notes"
            notes_dir.mkdir()
            (project_root / "wiki" / "topics").mkdir(parents=True)
            (project_root / "wiki" / "entities").mkdir(parents=True)
            (project_root / "briefs").mkdir()

            note = frontmatter.Post(
                "# 一个随手记的想法\n",
                title="想法测试",
                date="2026-07-28",
                source_type="own_thought",
                knowledge_role="personal_basis",
                tags=[],
                entities=[],
            )
            (notes_dir / "thought.md").write_text(frontmatter.dumps(note), encoding="utf-8")
            build_index(project_root)

            errors = validate_repository(project_root)
            self.assertEqual(errors, [])

    @staticmethod
    def write_note(path: Path) -> None:
        note = frontmatter.Post(
            "# Body\n",
            title=path.stem,
            date="2026-07-19",
            source_type="web",
            source_path="../raw/missing.md",
            source_url="https://example.com",
            knowledge_role="external_input",
            tags=[],
            entities=[],
        )
        path.write_text(frontmatter.dumps(note), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
