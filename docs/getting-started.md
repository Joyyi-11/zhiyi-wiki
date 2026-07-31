# 快速上手

用 5 步搭起你自己的知识库。前置：装好 Python 3.10+ 和 `python-frontmatter`（`pip install python-frontmatter`）。

## 1. 初始化

```bash
git clone https://github.com/Joyyi-11/zhixin-wiki.git my-kb
cd my-kb
cp templates/inbox.md thoughts/inbox.md   # 建立你的想法暂存（已被 gitignore，不会公开）
python scripts/build_index.py             # 生成初始 INDEX.md
python scripts/validate.py                # 确认空骨架有效
```

## 2. 写第一篇笔记（外部文章）

1. 把一篇文章全文存到 `raw/2026-07-28-某文章.md`（原料只读，后续不改）。
2. 复制 `templates/note-web.md` 到 `notes/2026-07-28-某文章.md`，填好 frontmatter 和正文。
3. `source_path` 指向 `../raw/2026-07-28-某文章.md`，`knowledge_role` 选 `external_input`。
4. `python scripts/build_index.py` 重建索引。

## 3. 写一篇个人文章笔记

把你自己已发表的文章存到 `articles/`，用 `templates/note-own-article.md`，`source_type: own_article`，`knowledge_role: personal_basis`。个人文章是你的基准，外部材料只能强化、补充、修正或反驳它。

## 4. 建第一个主题页

当至少两篇笔记形成可复用的共同判断时，复制 `templates/topic.md` 到 `wiki/topics/`。主题页必须包含：当前结论、边界与矛盾、挑战视角、待验证问题、来源。`sources` 列出来源笔记。

## 5. 验证与回顾

```bash
python scripts/validate.py        # 字段、来源、章节、索引一致性
python scripts/review.py          # 全库状态快照
```

## 日常循环

- 入库新材料 -> 写 notes -> 往回织进主题页 -> `build_index` -> `validate`。
- 想法随时记到 `thoughts/inbox.md`，定期整理成 `own_thought` 笔记。
- 想看库的整体状态跑 `review.py`。

完整规则见 [`AGENTS.md`](../AGENTS.md)，架构总览见 [`ARCHITECTURE.md`](../ARCHITECTURE.md)，方法论详解见 [`methodology.md`](methodology.md)。
