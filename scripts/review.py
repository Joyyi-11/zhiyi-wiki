"""生成知识库回顾报告：全库状态快照 + 该推进的主题。

不绑定周期。默认输出全库状态；传一个天数参数则附加「近 N 天」时间切片
（按笔记 frontmatter date，即原文发布/想法日期，不是入库日期）。

用法：
  python scripts/review.py        # 全库快照
  python scripts/review.py 30     # 全库快照 + 近 30 天切片
"""
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
import sys

import frontmatter

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_items(directory: Path) -> list[dict]:
    items = []
    for path in directory.glob("*.md"):
        with path.open(encoding="utf-8-sig") as markdown_file:
            document = frontmatter.load(markdown_file)
        items.append(document.metadata)
    return items


def parse_date(value: object) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return None


def main() -> int:
    slice_days = int(sys.argv[1]) if len(sys.argv) > 1 else None
    today = date.today()

    notes = load_items(PROJECT_ROOT / "notes")
    role_counts = Counter(metadata.get("knowledge_role", "未分类") for metadata in notes)
    type_counts = Counter(metadata.get("source_type", "未分类") for metadata in notes)

    topics = load_items(PROJECT_ROOT / "wiki" / "topics")
    by_status: dict[str, list[str]] = defaultdict(list)
    for metadata in topics:
        by_status[metadata.get("status", "unknown")].append(metadata.get("title", "无标题"))

    entities = load_items(PROJECT_ROOT / "wiki" / "entities")

    print("# 知识库回顾报告\n")
    print(f"生成日期：{today.isoformat()}\n")

    print("## 全库状态\n")
    print(f"- 笔记：{len(notes)} 篇")
    role_parts = [
        f"{role} {role_counts.get(role, 0)}"
        for role in ("personal_basis", "curated_influence", "external_input")
    ]
    print(f"  - knowledge_role：{' / '.join(role_parts)}")
    type_parts = [
        f"{source_type} {type_counts.get(source_type, 0)}"
        for source_type in ("web", "own_article", "own_thought")
    ]
    print(f"  - source_type：{' / '.join(type_parts)}")
    print(
        f"- 主题页：{len(topics)} 个"
        f"（developing {len(by_status.get('developing', []))}"
        f" / stable {len(by_status.get('stable', []))}）"
    )
    print(f"- 实体页：{len(entities)} 个")

    developing = by_status.get("developing", [])
    print("\n## 该编译或推进的主题\n")
    if developing:
        for title in sorted(developing):
            print(f"- {title}（developing，待推进或稳定）")
    else:
        print("- 暂无 developing 主题")

    if slice_days is not None:
        cutoff = today - timedelta(days=slice_days)
        recent = []
        for metadata in notes:
            note_date = parse_date(metadata.get("date"))
            if note_date and note_date >= cutoff:
                recent.append(
                    (note_date, metadata.get("title", "无标题"), metadata.get("knowledge_role", ""))
                )
        recent.sort(key=lambda item: item[0], reverse=True)

        print(f"\n## 近 {slice_days} 天切片（按笔记 date，即原文发布/想法日期）\n")
        print(f"共 {len(recent)} 篇：\n")
        if recent:
            for note_date, title, role in recent:
                print(f"- {note_date} · [{role}] {title}")
        else:
            print("- 暂无")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
