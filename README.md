# zhiyi-builder

> 织漪（zhiyi）：往回织，激起涟漪；谐音「质疑」——材料织入时激起层层更新，而每一个形成的判断都要被持续质疑。

一个以「编译大于检索」为核心的个人知识库方法论与骨架。以个人实践为锚，把外部材料往回织进主题判断，又主动逆着锚点找反例。纯文件，零数据库 / 零向量库 / 零 RAG。

## 为什么

大多数知识管理工具靠「收藏 + 检索」：信息越堆越多，需要时再搜。问题是收藏 ≠ 吸收，检索到的碎片也拼不成判断。

织漪反过来：**编译大于检索**。每条新材料都织进主题页、标矛盾、接受挑战，最终形成可复用的当前判断。问答时优先读编译层，不重扫原料。并以个人实践为锚，主动逆锚找反例，避免确认偏误。

## 核心理念

- **编译 > 检索**：不靠 RAG 临时拼结果，而是编译成主题页里的当前判断。
- **反确认偏误**：材料标注性质（支持/补充/修正/反驳），主题页强制「挑战视角」，以个人为锚又主动找反例。
- **往回织不往后堆**：新材料织进主题页，不堆孤岛。
- **原料只读**：`raw/`、`articles/` 永不改写。
- **机械归脚本，语义归 AI**。

## 快速上手

```bash
git clone <本仓库> my-kb
cd my-kb
pip install python-frontmatter
cp templates/inbox.md thoughts/inbox.md
python scripts/build_index.py
python scripts/validate.py
```

5 步写出第一篇笔记和主题页，见 [`docs/getting-started.md`](docs/getting-started.md)。

## 目录结构

```
raw/           完整原文（只读事实依据）
articles/      你已发表的个人文章原文（只读）
notes/         单源笔记（摘要/要点/标签/判断 + knowledge_role）
thoughts/      想法暂存 inbox.md（gitignore，不公开）
wiki/topics/   主题页（跨笔记的当前综合判断）
wiki/entities/ 实体页
briefs/        候选选题
scripts/       build_index.py / validate.py / review.py
templates/     笔记/主题/实体/选题/inbox 模板
docs/          快速上手 / 方法论 / 自定义
```

## 了解更多

- [架构总览](ARCHITECTURE.md)——进->存->取 数据流图
- [方法论](docs/methodology.md)——核心理念与 knowledge_role 三分
- [运行规则](AGENTS.md)——给 AI agent 的指令（语义层）
- [自定义](docs/customize.md)——标签体系、外部发现源、写作 Skill

## License

MIT
