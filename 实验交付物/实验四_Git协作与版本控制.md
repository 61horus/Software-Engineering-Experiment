# 实验四：Git 协作与版本控制

> 对应 SWEBOK 领域：软件配置管理（Software Configuration Management）
> 实验日期：2026-06-28

---

## 4.1 实验目标

本实验旨在掌握 Git 分布式版本控制的核心协作工作流，包括：

- **分支管理**：创建 feature 分支、合并策略选择
- **提交规范**：使用 Conventional Commits（feat/fix/docs/test/refactor/ci/chore/merge 前缀）
- **协作流程**：模拟多人并行开发 → 合并冲突 → 冲突解决
- **Pull Request 流程**：代码审查的基本要素

核心技术：Git 分支、merge（--no-ff）、冲突标记解析、git log --graph

---

## 4.2 实验过程

### 4.2.1 场景设计

模拟两名开发者并行工作：

| 角色 | 分支 | 任务 | 修改文件 |
|------|------|------|----------|
| 开发者 A | `feat/tags` | 为任务添加 `--tags` 标签字段 | task_model.py, task_service.py, main.py |
| 开发者 B | `feat/category` | 为任务添加 `--category` 分类字段 | task_model.py, task_service.py, main.py |

> 两人从同一基线（`097c211`）出发，修改相同的三个文件和相同的代码区域，必然产生合并冲突。

### 4.2.2 操作步骤

**Step 1 — 开发者 A 创建 tags 分支并实现功能**

```bash
git checkout -b feat/tags
# 修改 task_model.py / task_service.py / main.py
git add campus_task/
git commit -m "feat: add tags field to task model, CLI, and CSV export"
```

**Step 2 — 开发者 A 合并到 master（--no-ff 保留分支历史）**

```bash
git checkout master
git merge feat/tags --no-ff -m "merge: feat/tags branch — add --tags support to tasks"
```

此时 master 上已有了 `--tags` 功能。

**Step 3 — 开发者 B 创建 category 分支（基于合并前的 master）**

```bash
git checkout -b feat/category 097c211   # 切回合并前基线
# 修改 task_model.py / task_service.py / main.py（与 A 修改同一区域）
git commit -m "feat: add category field and filter to tasks"
```

**Step 4 — 开发者 B 尝试合并 → 冲突**

```bash
git checkout master
git merge feat/category
# Auto-merging campus_task/main.py
# CONFLICT (content): Merge conflict in campus_task/main.py
# Auto-merging campus_task/task_model.py
# CONFLICT (content): Merge conflict in campus_task/task_model.py
# Auto-merging campus_task/task_service.py
# CONFLICT (content): Merge conflict in campus_task/task_service.py
# Automatic merge failed; fix conflicts and then commit the result.
```

三个文件全部冲突，Git 在冲突位置插入标准标记：

```
<<<<<<< HEAD
    p_add.add_argument("--tags", default="", help="任务标签，多个用逗号分隔")
=======
    p_add.add_argument("--category", default="general", ...)
>>>>>>> feat/category
```

**Step 5 — 手工解决冲突**

策略：保留两个功能（不是二选一），合并参数列表和数据结构：

- `task_model.py`：`create_task()` 同时接受 `tags` 和 `category`，返回 dict 包含两个字段
- `task_service.py`：`add_new_task()` 传递两个参数
- `main.py`：命令行同时暴露 `--tags` 和 `--category`，列表展示两者

```bash
# 手工编辑三个文件，删除冲突标记，合并两边代码
git add campus_task/task_model.py campus_task/task_service.py campus_task/main.py
git commit -m "merge: resolve conflict — integrate both --tags and --category features"
```

### 4.2.3 最终分支拓扑

```
*   8ace782 merge: resolve conflict — integrate both --tags and --category features
|\
| * d88882c feat: add category field and filter to tasks          (feat/category)
* |   9599c45 merge: feat/tags branch — add --tags support         (merge --no-ff)
|\ \
| |/
| * d87c749 feat: add tags field to task model, CLI, and CSV export (feat/tags)
|/
* 097c211 docs: 实验报告规范新增标题样式/目录/折叠/编辑要点四节        (基线)
```

> 关键特征：两个 feature 分支各自独立提交，最终通过手工冲突解决合并到 master，保留了完整的分支历史和 `--no-ff` 合并提交。

---

## 4.3 核心交付物

### 4.3.1 提交信息规范展示

本仓库全量提交均使用 Conventional Commits 前缀：

| 前缀 | 含义 | 本仓库使用次数 |
|------|------|:---:|
| `feat` | 新功能 | 4 |
| `fix` | 缺陷修复 | 3 |
| `docs` | 文档变更 | 6 |
| `test` | 测试相关 | 1 |
| `refactor` | 重构 | 5 |
| `ci` | CI 配置 | 1 |
| `chore` | 杂项维护 | 2 |
| `merge` | 合并提交 | 2 |

示例：
```
feat: add tags field to task model, CLI, and CSV export
fix: export CSV目录自动创建 + 截图命令清单
test: 实验三 - 11个pytest测试用例
refactor: argparse替代sys.argv + 日志 + --version + 用户手册（实验七 v0.4.0）
merge: resolve conflict — integrate both --tags and --category features
```

### 4.3.2 分支协作规范

| 规范项 | 实践 |
|--------|------|
| 主分支 | `master`（非 main） |
| 功能分支命名 | `feat/<描述>` |
| 合并策略 | `--no-ff`（保留分支提交历史） |
| 冲突解决 | 手工合并 → `git add` → `git commit` |
| 每人独立分支 | feat/tags（A）、feat/category（B） |

### 4.3.3 PR / 代码审查流程

虽然本项目为单人作业无法做真正的 PR，但完整模拟了 PR 的核心要素：

1. **分支隔离**：每个功能在独立分支开发，不直接修改 master
2. **合并前审查**：merge 时 Git 自动检测冲突并阻止合并
3. **冲突解决记录**：冲突解决过程记录在 merge commit message 中
4. **历史可追溯**：`git log --graph` 清晰展示谁在何时做了什么

实际团队协作中，上述流程对应为：
- 开发者 push feature 分支到远程
- 在 Gitee/GitHub 创建 Pull Request
- 队友 Review 代码后 approve
- 合并时若冲突，由 PR 作者解决后 force-push 更新

### 4.3.4 合并冲突解决说明

**冲突成因**

两个分支修改了同一文件的同一区域：

| 文件 | HEAD (feat/tags 已合并) | feat/category | 冲突位置 |
|------|------------------------|---------------|----------|
| task_model.py:L8 | `tags: str = ""` | `category: str = "general"` | 函数签名 |
| task_model.py:L24 | `"tags": tag_list` | `"category": category` | 返回 dict |
| task_service.py:L10 | `tags: str = ""` | `category: str = "general"` | 函数签名 |
| main.py:L72 | `--tags` argument | `--category` argument | argparse 注册 |
| main.py:L48 | 显示 tags | 显示 category | 输出格式 |
| main.py:L106 | 传递 tags | 传递 category | add 调用 |

**解决策略**

不是二选一，而是**同时保留两个字段**：
- 函数签名扩展为同时接受 `tags` 和 `category`
- 返回 dict 包含两个字段
- 命令行同时暴露两个选项
- CSV 导出包含两列

**通用冲突解决原则**
1. 理解两边改动的意图（不要机械合并）
2. 优先"都保留"而非"二选一"
3. 解决后运行测试确保功能不退化
4. commit message 中说明冲突原因和解决方式

---

## 4.4 运行结果

### 4.4.1 合并后功能验证

```bash
$ python -m campus_task --version
CampusTask v0.5.0

$ python -m campus_task add "实验四演示" --tags "软工,Git" --category "实验" \
    --deadline 2026-07-10 --priority high
✅ 任务已添加：[4] 实验四演示

$ python -m campus_task list
  [4] ⏳ 实验四演示
      状态: pending  |  优先级: high  |  分类: 实验  |  截止: 2026-07-10
      标签: 软工, Git
      创建时间: 2026-06-28 14:00:00
```

> 两个功能（tags + category）同时工作，冲突解决后功能无退化。

### 4.4.2 Git 完整历史

```
$ git log --oneline --graph --all -15
*   8ace782 merge: resolve conflict — integrate both --tags and --category features
|\
| * d88882c feat: add category field and filter to tasks
* |   9599c45 merge: feat/tags branch — add --tags support to tasks
|\ \
| |/
| * d87c749 feat: add tags field to task model, CLI, and CSV export
|/
* 097c211 docs: 实验报告规范新增标题样式/目录/折叠/编辑要点四节
* 322b975 docs: 完善实验报告规范 ...
...
```

---

## 4.5 实验结果自评

| 评分项 | 满分 | 自评 | 依据 |
|--------|:--:|:--:|------|
| 提交信息规范（feat/fix/docs前缀） | 25 | 25 | 全仓库 24 次提交全部使用 Conventional Commits 前缀，无一例外 |
| 分支协作规范（每人独立分支） | 25 | 25 | 创建 feat/tags 和 feat/category 两个独立分支，模拟两人并行开发，--no-ff 合并保留历史 |
| PR/代码审查流程有效 | 25 | 22 | 完整模拟了分支隔离→合并冲突→审查→解决的流程，但缺少真正的 PR 界面截图（单人作业限制） |
| 合并冲突解决说明 | 25 | 25 | 详细记录了 3 文件 × 多处冲突的成因、标记解析、解决策略和验证过程 |

**总分：97/100**

扣分说明：PR 审查环节因单人作业无法做真正的跨开发者 Review，扣 3 分。其余三项满分——提交规范贯彻始终，分支工作流完整可复现，冲突解决有据可查。

---

## 4.6 课后反思

**问题一：`--no-ff` 合并和 fast-forward 合并有什么区别？各适用于什么场景？**

`--no-ff`（no fast-forward）会**始终创建一个新的合并提交**，保留分支的历史轨迹。fast-forward 则在目标分支没有新提交时，直接将指针移到 feature 分支的最新提交，**不产生合并提交**，历史呈线性。

适用场景：
- `--no-ff`：团队协作、需要追踪"这个功能是在哪个分支开发的"、代码审查需要明确的合并点
- fast-forward：个人项目、小修改、希望保持线性历史的场景

本仓库选用 `--no-ff` 的原因：课程要求展示分支协作痕迹，线性历史无法体现分支工作。

**问题二：合并冲突在什么情况下发生？如何系统性地解决？**

合并冲突发生在两个分支**修改了同一文件的同一区域**时——Git 无法判断应该保留哪个版本。冲突的本质是"同一块代码有两个不同的演进方向"。

系统性解决流程：
1. `git status` 查看冲突文件列表
2. 打开每个冲突文件，搜索 `<<<<<<<` 标记
3. 理解两边意图：HEAD（当前分支）vs 合并进来的分支
4. 选择策略：保留一方、保留两方、或重新编写
5. 删除冲突标记（`<<<<<<<` / `=======` / `>>>>>>>`）
6. `git add` 标记已解决
7. `git commit` 完成合并
8. 运行测试验证

本次实践中三个文件冲突的策略是"两方都保留"，因为 tags 和 category 是正交的功能，不应二选一。

**问题三：本仓库的 commit message 规范（feat/fix/docs...）相比随意写 message 有什么优势？**

1. **可检索性**：`git log --grep="feat:"` 一键列出所有新功能，不用读每条 message
2. **自动化 CHANGELOG**：standard-version 等工具可自动按前缀生成版本发布说明
3. **语义清晰**：reviewer 一眼就知道这个 commit 是新增功能、修 bug 还是纯文档
4. **粒度约束**：强制开发者在提交前思考"这个 commit 到底是什么类型"，避免"一次提交改了一堆不相关的东西"
5. **团队约定**：统一的规范意味着统一的预期，降低沟通成本

本仓库 24 次提交坚持使用前缀规范，最终可以按类型统计：4 feat + 3 fix + 6 docs + 1 test + 5 refactor + 1 ci + 2 chore + 2 merge。这就是一份自动生成的工作量分布报告。
