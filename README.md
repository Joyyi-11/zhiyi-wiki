# Zhiyi（织漪）

> 织漪（zhiyi）：往回织，激起涟漪；谐音「质疑」——材料织入时激起层层更新，而每一个形成的判断都要被持续质疑。

一个以「编译大于检索」为核心的个人知识 wiki 方法论与骨架。它在材料存入时就把个人实践、外部经验和想法编译进已有主题，持续形成和校正可复用的当前判断，而不是先堆资料、等使用时再临时检索和拼接。

> 灵感来自于 Andrej Karpathy 的 LLM Wiki。

当前仓库是可复用骨架和方法论，不包含私人知识库内容；你可以把它 clone 成自己的 `zhiyi-wiki` 实例。

## 为什么

传统个人知识管理通常采用「先收藏、用时检索」的流程：文章、笔记和链接先存进去，等写作、决策或回答问题时再搜索和拼接。这个流程擅长保存材料，却容易产生两个问题：收藏不等于吸收，检索到的碎片也不会自动变成自己的判断。

织漪把关键动作前移到「存」：每条确认入库的新材料都要回到已有主题，说明它补充、扩展、修正还是反驳了什么，并据此更新主题页里的当前判断。这里的「往回织」不是继续往后新增一篇孤立笔记，而是把新材料编回已有知识关系。

编译以个人实践、已有想法和已发表内容为认知基准，但不把它们当成不可挑战的结论。材料入库时必须标明它与现有判断的关系，主题页还要主动保留矛盾、反例和待验证问题，以此防止只收集支持自己的证据。

因此，织漪的流程不是「收藏 -> 检索 -> 临时拼接」，而是：

```text
进：发现并确认值得处理的材料
  -> 存：保存原料，写成单源笔记，往回织入主题判断
  -> 取：优先读取已经编译的主题页，需要核对事实时再回到原料
```

## 核心理念

- **编译 > 检索**：不靠 RAG 临时拼结果，而是编译成主题页里的当前判断。
- **以个人认知为基准**：先明确自己的实践和已有判断，再判断外部材料带来了什么认知增量。
- **防止确认偏误**：材料标注性质（支持/补充/修正/反驳），主题页保留挑战视角、矛盾和待验证问题。
- **往回织不往后堆**：新材料必须融入并更新已有主题判断，不继续制造孤岛笔记。
- **原料只读**：`raw/`、`articles/` 永不改写。
- **机械归脚本，语义归 AI**。

## 各部分分工

| 部分 | 负责什么 |
|------|----------|
| 使用者 | 决定什么值得入库、个人认知基准是什么，并对最终判断负责 |
| AI agent | 摘要、识别材料性质、发现矛盾、提出主题更新方案，完成语义层的「往回织」 |
| Python 脚本 | 构建索引，校验元数据、来源关系和主题页结构，回顾知识库状态 |
| Markdown 文件 | 保存原料、单源笔记和主题判断，是可阅读、可迁移、可版本控制的真实源 |

整个系统使用纯文件、Markdown 和 frontmatter，不依赖数据库、向量库或 RAG。问答时优先读取已经编译的主题页，而不是每次重新扫描全部原料。

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
