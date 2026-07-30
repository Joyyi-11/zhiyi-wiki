# Zhiyi（织漪）

> 织漪（zhiyi）：往回织，激起涟漪；谐音「质疑」——材料织入时激起层层更新，而每一个形成的判断都要被持续质疑。

一个以「编译大于检索」为核心的个人知识 wiki 方法论与骨架。它用纯文件、Markdown 和 AI agent，把个人实践、外部材料和想法编译成可复用的主题判断，而不是把资料越堆越多、需要时再临时搜索。

> 灵感来自于 Andrej Karpathy 的 LLM Wiki。

当前仓库是可复用骨架和方法论，不包含私人知识库内容；你可以把它 clone 成自己的 `zhiyi-wiki` 实例。

## 为什么

大多数知识管理工具靠「收藏 + 检索」：信息越堆越多，需要时再搜。问题是收藏 ≠ 吸收，检索到的碎片也拼不成判断。

织漪反过来：**编译大于检索**。每条新材料都织进主题页、标矛盾、接受挑战，最终形成可复用的当前判断。问答时优先读编译层，不重扫原料。并以个人实践为锚，主动逆锚找反例，避免确认偏误。

## 核心理念

- **编译 > 检索**：不靠 RAG 临时拼结果，而是编译成主题页里的当前判断。
- **反确认偏误**：材料标注性质（支持/补充/修正/反驳），主题页强制「挑战视角」，以个人为锚又主动找反例。
- **往回织不往后堆**：新材料织进主题页，不堆孤岛。
- **原料只读**：`raw/`、`articles/` 永不改写。
- **机械归脚本，语义归 AI**。

## Agent 入口

- [`SKILL.md`](SKILL.md)：通用方法论入口，适合安装为 Skill 或喂给任意 agent。
- [`AGENTS.md`](AGENTS.md)：本仓库内的 agent 运行规则，用于约束入库、往回织、问答、选题和验证。

## 快速上手

```bash
git clone https://github.com/Joyyi-11/zhiyi-wiki.git my-kb
cd my-kb
pip install python-frontmatter
cp templates/inbox.md thoughts/inbox.md
python scripts/build_index.py
python scripts/validate.py
```

5 步写出第一篇笔记和主题页，见 [`docs/getting-started.md`](docs/getting-started.md)。

## 最小例子

```text
notes/2026-07-01-my-practice.md      knowledge_role: personal_basis
notes/2026-07-02-external-article.md knowledge_role: external_input
wiki/topics/ai-collaboration.md      综合两篇笔记，写出当前结论、边界、挑战视角和待验证问题
```

问答时先读 `INDEX.md` 和主题页；只有需要核对具体事实时才回到单源笔记和原料。

## 脚本约束

- `scripts/build_index.py`：生成 `INDEX.md`，按知识角色组织目录。
- `scripts/validate.py`：校验 frontmatter、来源路径、主题页必选章节和索引一致性。
- `scripts/review.py`：输出全库状态和可推进主题，不自动改写内容。

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
- [Skill 入口](SKILL.md)——可复用方法论与 agent 工作流
- [运行规则](AGENTS.md)——本仓库内的 agent 指令（语义层）
- [自定义](docs/customize.md)——标签体系、外部发现源、写作 Skill

## 作者

连漪（Lianyi）

## 许可证

MIT
