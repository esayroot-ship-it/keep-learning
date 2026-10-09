# Keep Learning

一个面向 Codex 的实用学习技能：先用简短问题确定起点，再用几小时建立某个主题的常用操作能力，让学习者能够理解基本原理、独立完成正常工作，并验证自己的结果。

教学主线是 **基础细讲 → 常用任务简讲 → 扩展只给方向**。语言和 SQL 用读写代码练习，系统与工具用实际操作，架构用流程、约束和故障场景分析；文字、图示和交互网页按内容选择。

本仓库包含技能指令、按需读取的教学规范、Python 本地进度管理脚本及回归测试。技能入口是 [SKILL.md](SKILL.md)，当前采用显式调用，不会仅因普通问答涉及技术知识就自动启动课程。

## 导航

- [核心理念](#核心理念)
- [快速开始](#快速开始)
- [用法示例](#用法示例)
- [学习流程](#学习流程)
- [训练模式](#训练模式)
- [读写代码的练习规则](#读写代码的练习规则)
- [教学内容与媒介](#教学内容与媒介)
- [本地学习进度](#本地学习进度)
- [脚本与命令](#脚本与命令)
- [配置与默认值](#配置与默认值)
- [目录结构](#目录结构)
- [更新与验证](#更新与验证)
- [常见问题](#常见问题)
- [教学设计参考](#教学设计参考)

## 核心理念

### 以正常工作为边界

规划先明确角色、环境和要完成的任务，再决定学什么。例如，应用开发中的数据库学习重点是数据建模、语句、事务、索引使用和常见错误；存储引擎实现或集群架构只有在目标需要时才进入必修范围。

课程以覆盖约 **95% 的约定范围内常用应用需求** 为设计目标。这个数字不代表覆盖学科全部知识，也不是凭几个练习就能证明的统计结果。没有代表性的使用数据时，技能会列明常用场景和未覆盖部分，不虚报完成比例。

### 几小时建立可用能力

- 主题课程默认约 **3 小时**，通常按 **2–4 小时**规划，包含讲解、必要练习和验证。
- 一个小单元通常约 **5–15 分钟**；简单问题可以几句话解决，不强行做成课程。
- 边界确认通常只有一轮、1–3 个简短问题。已有的信息会复用，不反复采访。
- 先讲操作所需的基本原理和常见失败，再按实际缺口补充；不默认展开完整底层实现。
- 单元结尾最多给出两条简短扩展方向，说明什么时候值得继续学，不自动追加作业或章节。

时间是规划预算。遇到关键先修缺口时，应说明剩余工作，不能为了准时结束就把未掌握内容登记为掌握。用户明确指定的范围和时间优先。

### 用独立表现判断掌握

看过讲解、运行过 AI 提供的代码、点完网页，都不等于独立掌握。学习者需要在适当的任务中作出选择、完成操作或推理，并检查结果。允许查文档；不把背诵所有命令和 API 当作学习目标。

完整范围规则见 [课程范围与时间](references/curriculum-quality.md)，起点判断见 [教学设计](references/teaching-design.md)。

## 快速开始

### 环境要求

- 能加载本地 Agent Skills 的 Codex 环境。
- Git：用于克隆和更新本仓库。
- Python **3.10+**：运行本地管理脚本和测试时需要，脚本仅使用标准库。

普通对话教学主要由技能指令驱动。具体课程需要的解释器、数据库或其他工具，由该课程单独确定；本仓库不会自动安装这些环境。

### 安装

将仓库克隆到 Codex 的技能目录，保持 `keep-learning/SKILL.md` 及其相邻目录完整。当前官方文档列出的用户级目录是 `~/.agents/skills`，项目级目录是 `.agents/skills`。[官方技能文档](https://learn.chatgpt.com/docs/build-skills)

**Windows PowerShell：**

```powershell
$skillParent = Join-Path $HOME ".agents\skills"
New-Item -ItemType Directory -Force -Path $skillParent | Out-Null
git clone https://github.com/esayroot-ship-it/keep-learning.git (Join-Path $skillParent "keep-learning")
```

**Windows CMD：**

```bat
if not exist "%USERPROFILE%\.agents\skills" mkdir "%USERPROFILE%\.agents\skills"
git clone https://github.com/esayroot-ship-it/keep-learning.git "%USERPROFILE%\.agents\skills\keep-learning"
```

**macOS / Linux：**

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/esayroot-ship-it/keep-learning.git ~/.agents/skills/keep-learning
```

只选适合当前环境的一种方式。如果已有同名技能或使用自定义技能目录，先确认现有安装位置并保留本地修改，避免重复安装。私有仓库的克隆需要相应访问权限。

安装后在技能选择器中找到 **Keep Learning**，或在 Codex CLI / IDE 中通过 `$keep-learning` 显式调用。若新技能没有显示，可以重启 Codex 后检查。[官方调用与发现说明](https://learn.chatgpt.com/docs/build-skills)

`agents/openai.yaml` 保留了 `allow_implicit_invocation: false`。本仓库是独立技能，不需要额外的 MCP 服务或后台服务。

## 用法示例

### 从零学习一个常用主题

```text
使用 $keep-learning 学习 Linux 常用操作。
我几乎零基础，希望能独立处理日常文件、软件和远程操作。
先用很短的问题确定起点，按几个小时的规模规划。
```

### 只检查教学方案

```text
使用 $keep-learning 规划 Python 文件处理的学习路线。
只给单元、要学的内容、练习方式和预计时间，不生成课程文件或网页。
```

### 练习独立编写

```text
使用 $keep-learning 帮我独立写出 JSON 数据筛选逻辑。
我能读懂简单代码，但自己写比较困难。
先教必要知识，再给一个没有讲过答案的小任务。
```

### 阅读现有代码

```text
使用 $keep-learning 帮我读懂 src/cache.py 的查询路径。
逐步解释入口、调用顺序、数据变化和异常，然后用新情况检查我的理解。
本次只练阅读，不要求重写代码。
```

### 学习架构与取舍

```text
使用 $keep-learning 学习单机应用中的缓存一致性设计。
以请求流程、数据状态和常见失败场景为主。
只有交互能帮助理解时才生成网页，不扩展到大规模分布式架构。
```

### 保存和继续学习

```text
使用 $keep-learning 继续这个学习任务，并维护本地进度。
记录实际完成的练习、尚未理解的点和下一步，不重置此前的记录。
```

也可以明确说“不要提问，按零基础开始”。技能会说明假定的起点，不会把未评估的能力写成已经确认。

## 学习流程

1. **限定目标**：明确正常工作中要完成什么，复用已有信息。
2. **快速判断起点**：用短问题或已有代码、操作记录定位当前缺口。
3. **规划有限路线**：列出常用任务、必要原理、时间、媒介和独立验收，标明扩展方向。
4. **选择训练模式**：每个单元选一种主模式，不要求所有内容都写代码。
5. **讲解并应用**：给必要基础和最小示例，再让学习者处理未讲过的情况。
6. **验证与修正**：根据实际表现补最小缺口，复用已有成果，避免重复练习。
7. **继续或结束**：完成当前单元后推进到下一个核心单元；已授权本地跟踪时同步记录。

学习在当前 Agent 内完成，不派生子智能体。规则和范例按触发条件读取，避免每次加载全部参考文档。

## 训练模式

| 模式 | 适合内容 | 主要学习产物 | 验收关注点 |
| --- | --- | --- | --- |
| `manual-coding` 独立编写 | 语言、SQL、脚本、测试、小型修改 | 从需求写出的实现及一个有意义的变化 | 解释、预测、修改、独立编写、验证 |
| `code-reading` 代码阅读 | 已有函数、调用链、行为定位、修改影响 | 执行追踪、状态变化说明、影响分析 | 解释、追踪、预测、影响、验证 |
| `conceptual` 原理概念 | 协议、机制、数学或运行模型 | 模型、比较、对新场景的推理 | 解释、建模、比较、应用、验证 |
| `operational` 操作实践 | Linux、开发工具、部署、中间件管理 | 实际操作和状态、日志等结果 | 解释、步骤、执行、诊断、验证 |
| `architecture` 架构设计 | 系统边界、请求流程、可靠性、方案选择 | 有边界的设计、流程图、取舍与失败分析 | 解释、追踪、取舍、设计、验证 |

任务级别可以使用 `auto` 或 `mixed`。它们表示自动选择或组合模式，具体单元仍须选定上述五种模式之一。阅读与编写可以共用上下文，但分别保留证据；读懂不能自动证明会写。

权威规则见 [训练模式](references/training-modes.md)。

## 读写代码的练习规则

**编写练习控制在最小有效规模。** 优先选择一个表达式、函数、查询或小补丁；提供无关的环境准备和调用代码，把核心选择留给学习者。通常用一次独立实现和一次有意义的需求变化完成检查，不把五类验收变成五份作业。

提示从概念逐步增加到伪代码和部分实现。若已经给出关键算法、分支或核心骨架，该次练习属于有帮助的练习，需要一个新的小变式才能验证独立性。

**阅读练习按实际复杂度递进：**

1. 表达式或短顺序片段。
2. 带分支、循环或相关错误路径的单个函数。
3. 同文件内多个函数的调用与状态。
4. 相关文件之间的一条有限执行路径。
5. 陌生实现中的需求、故障或改动分析。

每次只提高一个主要难度维度。帮助也从完整示范，逐步减少到提示入口，再到独立追踪；不以代码行数作为难度，也不把陌生语法当成隐藏考题。

详见 [独立编写](references/code-writing.md)、[分级阅读](references/code-reading.md)和 [先修控制](references/prerequisite-control.md)。

## 教学内容与媒介

| 学习问题 | 默认表达方式 |
| --- | --- |
| 定义、语法、一步操作 | 连贯文字与一个最小例子 |
| 代码执行与数据变化 | 真实代码、调用路径、值或状态追踪 |
| 依赖关系、比较与结构 | 简图、表格或 Mermaid |
| 并发顺序、状态变化、参数影响 | 必要时使用可操纵的交互实验 |
| 架构选择 | 约束、流程、取舍表和失败场景 |

需要网页时，默认使用原生 HTML、CSS、JavaScript，优先本地可打开的页面。交互必须改变有意义的状态，并显示结果；不为简单知识强行建设网站。

多阶段教学中，文字或 Markdown 负责完整解释、操作要求与参考；网页负责可操纵的状态和过程。二者使用一致案例和单元标识，相关内容互相指向。模拟、真实实验和已经验证的行为会明确区分。

具体约束见 [自适应呈现](references/adaptive-presentation.md)。

## 本地学习进度

只有在要求保存进度、跨会话继续，或已经授权本地跟踪时，才创建和维护学习项目。普通问答、只规划以及修改技能本身，不会自动生成课程工程。

```text
<学习根目录>/<目标名称>/
├── 00-meta/
│   └── learning-config.json       # 目标、偏好与完成条件
├── 01-lessons/
│   ├── current.md                 # 当前教学内容
│   └── archive/                   # 已完成教学的归档
├── 02-practice/
│   ├── current.md                 # 当前练习
│   └── archive/
├── 03-evidence/
│   ├── submitted/                 # 学习者提交的成果
│   ├── reviewed/                  # 实际表现与帮助记录
│   └── reference/                 # 参考材料
└── 04-status/
    ├── progress.json              # 单元状态、检查、缺口与下一步
    ├── overview.md                # 自动生成的概览
    ├── next-actions.md
    ├── completed.md
    ├── blocked.md
    ├── history.jsonl
    └── backups/
```

配置、进度和证据各有唯一归属；Markdown 状态页由真实记录生成。中央索引位于 `$CODEX_HOME/learning/registry.json`，未设置 `CODEX_HOME` 时使用 `~/.codex/learning/registry.json`。技能安装目录与学习数据目录互相独立。

管理工具支持登记、切换、续学、快照、恢复和归档。更新使用锁和快照；失败的推进会恢复状态。归档隐藏索引条目并保留文件，续学不会清空已有记录。

详见 [本地管理](references/local-management.md)和 [数据布局](references/workspace.md)。

## 脚本与命令

以下命令从本仓库根目录或技能安装目录执行。Windows PowerShell / CMD 使用 `python`；macOS / Linux 按环境使用 `python3`。通常让 Agent 根据实际学习证据调用即可，不必手工维护 JSON。

### 创建、查看与继续

```text
python -X utf8 scripts/manage_learning.py create --goal "Linux 常用操作" --root "learning-workspace" --training-mode auto
python -X utf8 scripts/manage_learning.py list
python -X utf8 scripts/manage_learning.py status
python -X utf8 scripts/manage_learning.py --compact status
python -X utf8 scripts/manage_learning.py resume
```

`--root` 可指定自己管理的学习目录。创建同名已有目录会被拒绝；已有任务应使用 `register` 或 `resume`。`--compact` 只缩短响应，不减少保存的数据或验收检查。

### 安排一个单元并记录真实进展

```text
python -X utf8 scripts/manage_learning.py update -- --plan-unit "files=文件操作" --training-mode "files=operational" --advance
python -X utf8 scripts/manage_learning.py record --text "已完成路径练习；相对路径判断仍需进一步检查。"
python -X utf8 scripts/manage_learning.py update -- --gap "相对路径的起点" --next "解释并验证改变当前目录后的路径"
```

这些例子操作当前选中的任务。需要指定其他任务时，使用该子命令的 `--workspace <目录>` 或 `--task <任务ID>`。`update` 的 `--` 后参数传给进度助手。

记录笔记不会自动标记掌握。审核后的检查用 `record --check ...` 登记；独立编写与独立阅读追踪还需要 `--independent` 和实际证据。所有必要检查通过、缺口解决后，才使用 `update -- --advance` 完成归档和推进。

| 命令 | 用途 |
| --- | --- |
| `create` | 新建任务并登记、选中 |
| `register` | 登记并选中已有兼容任务 |
| `list` / `list --all` | 列出任务；后者包括已归档任务 |
| `status` | 只读查看状态 |
| `resume` | 选中任务并生成概览，继续当前学习 |
| `record` | 记录实际回答、成果、帮助与已审核的检查 |
| `update` | 调整单元、依赖、缺口和下一步，执行受检查约束的推进 |
| `restore --snapshot <路径>` | 从有效快照恢复，并为恢复前状态保留快照 |
| `archive` / `unarchive` | 归档或恢复索引条目，保留学习文件 |

`init_learning_workspace.py` 负责初始化，`update_progress.py` 负责底层状态转换。日常维护优先通过 `manage_learning.py`，以保留审核、锁、快照和恢复流程。

查看完整参数：

```text
python -X utf8 scripts/manage_learning.py --help
python -X utf8 scripts/manage_learning.py record --help
python -X utf8 scripts/init_learning_workspace.py --help
python -X utf8 scripts/update_progress.py --help
```

## 配置与默认值

| 设置 | 默认行为 |
| --- | --- |
| 主题时长 | 约 3 小时，明确指定的预算优先 |
| 未知能力 | `unassessed`，不直接认定已经掌握或完全不会 |
| 训练模式 | `auto`，为每个单元选定具体模式 |
| 解释细节 | `standard`，补足当前应用所需的因果关系 |
| 单元主要新概念 | 1 个，配置范围为 1–3 个 |
| 提问 | 通常一个主问题；尊重不提问要求 |
| 提示 | `hints-first`，独立练习答案与教学示例分开 |
| 待执行单元窗口 | 默认 5 个，允许 3–7 个；不足时不凑数 |
| 工程扩展 | `on-request`，需要时才展开 |
| 持久化 | 按用户要求启用 |

当前指令优先于已保存偏好，已保存偏好优先于技能默认值。默认值更新不会重置已有课程或历史证据。完整字段见 [学习配置](references/learning-parameters.md)。

## 目录结构

```text
keep-learning/
├── README.md
├── SKILL.md
├── agents/openai.yaml
├── references/                    # 18 份按需读取的规则与范例
├── scripts/
│   ├── init_learning_workspace.py
│   ├── manage_learning.py
│   └── update_progress.py
└── tests/
    ├── test_learning_progress.py
    └── test_local_management.py
```

| 需要了解的内容 | 参考文件 |
| --- | --- |
| 任务规模、起点与教学路径 | [task-model](references/task-model.md)、[teaching-design](references/teaching-design.md) |
| 范围、时间与覆盖目标 | [curriculum-quality](references/curriculum-quality.md) |
| 视频教学方法逆向范例 | [practical-course-example](references/practical-course-example.md) |
| 训练模式与读写能力 | [training-modes](references/training-modes.md)、[code-writing](references/code-writing.md)、[code-reading](references/code-reading.md) |
| 教学、提问、深度与先修 | [teaching-and-drills](references/teaching-and-drills.md)、[diagnostic-questioning](references/diagnostic-questioning.md)、[teaching-depth](references/teaching-depth.md)、[prerequisite-control](references/prerequisite-control.md) |
| 文字、图示与网页分配 | [adaptive-presentation](references/adaptive-presentation.md) |
| 推进、本地管理与配置 | [autonomous-progression](references/autonomous-progression.md)、[local-management](references/local-management.md)、[workspace](references/workspace.md)、[learning-parameters](references/learning-parameters.md) |
| 按需探索的领域与工程方向 | [capability-map](references/capability-map.md)、[engineering-expansion](references/engineering-expansion.md) |

## 更新与验证

在 Git 安装或开发副本中更新前，先确认本地修改，再进行快进更新：

```text
git status --short
git pull --ff-only
```

若安装目录是从开发仓库复制出来的，它是独立副本，修改开发仓库不会自动同步到安装目录。更新时先保存安装副本中的自定义修改，再明确同步需要更新的技能文件。学习数据不应混入技能发布内容。

运行现有测试：

```text
python -B -X utf8 -m unittest discover -s tests -v
```

当前包含 29 项测试，覆盖模式专属检查、读写证据分离、缺口阻止完成、归档失败恢复、旧进度兼容、本地索引、锁、快照恢复和精简输出。测试使用临时工作区和临时索引，不使用真实学习记录。

修改教学规则后，还应人工核对典型请求的范围、先修、媒介和验收是否合理。脚本测试验证状态行为，不能证明真实学习者在几小时内已经达到预期水平。

`.gitignore` 排除了 Python 缓存、虚拟环境、环境配置、默认学习工作区和字幕资料。仓库发布内容只有技能与维护资源；不会附带个人进度或视频字幕全文。

## 常见问题

**能保证几小时精通整个领域吗？**

目标是约定角色下的常用工作能力。若目标过大或先修不足，技能应指出范围与时间不匹配，而不是压缩成一份看似完整的目录。

**架构学习也要写代码吗？**

不强制。架构单元通过流程、约束、方案取舍和失败场景验收；只有目标本身要求实现时才安排编写单元。

**每个单元都有网页吗？**

没有。文字、代码或简单图示已经足够时就使用它们，交互页面服务于需要操纵状态或顺序的问题。

**脚本能自动判断我是否掌握了吗？**

不能。脚本保存经过审核的证据和状态，并检查推进条件；对回答和成果的判断仍由教学过程完成。

**必须回答问题或保存进度吗？**

都可以通过当前指令调整。直接讲解时会注明假定起点；未要求跟踪时，学习可以留在对话中。

**能用于其他支持 Agent Skills 的工具吗？**

核心指令与参考文档可以参考使用，但 `agents/openai.yaml` 是 Codex 配置，其他宿主的发现和调用方式需要按其规则适配。本仓库不宣称已验证所有宿主。

## 教学设计参考

本技能的实践范例参考 ChrisKim_ZHT 的 [《只学够用的 Linux：长度正好的零基础入门教程》](https://www.bilibili.com/video/BV13ctf6RECM/)及其[文字版](https://www.zouht.com/4399.html)，提炼受众边界、分层讲解、任务引入原理和简短扩展方向。

范例明确区分视频实际讲解与技能增加的独立练习、边界确认和本地跟踪。引用保留来源，仓库不复制课程字幕全文；参考作品的许可不等同于为本仓库另行授予许可。
