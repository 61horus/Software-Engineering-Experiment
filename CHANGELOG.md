# CHANGELOG

## [v0.5.0] - 2026-06-28

### 新增功能
- **任务标签**：`add` 命令支持 `--tags "标签1,标签2"`，逗号分隔多个标签
- **任务分类**：`add` 命令支持 `--category` 参数（general / 作业 / 实验 / 考试 / 其他）
- 任务列表和 CSV 导出同步展示 tags 和 category 字段

### 实验四完成
- Git 协作工作流演示：双分支并行开发 → 合并冲突 → 手工解决
- 提交信息规范贯穿全部 24+ 次提交（Conventional Commits）
- 文档交付物：实验四_Git协作与版本控制.md

---

## [v0.4.0] - 2026-06-14

### 新增功能
- **argparse 命令行解析**：替代 sys.argv，支持子命令和 --help
- **--version**：显示版本号
- **export CSV**：`export <文件路径>` 导出任务到 CSV 文件
- **日志系统**：操作日志写入 campus_task.log

### 文档
- USER_GUIDE.md 用户手册
- CHANGELOG.md 版本变更日志

---

## [v0.3.0] - 2026-06-14

### 新增功能
- **搜索任务**：`search <关键字>` 按标题关键字搜索任务
- **显示逾期任务**：`overdue` 命令显示截止日期已过的未完成任务
- **按状态筛选**：`list pending` / `list done` 按状态过滤
- **截止日期和优先级**：`add` 命令支持 `--deadline DATE` 和 `--priority high|medium|low`

### 变更
- 数据模型新增 `deadline` 和 `priority` 字段
- 任务列表显示增加优先级和截止日期列
- 版本号更新为 v0.3.0

### 测试
- 新增 5 个测试用例（搜索、逾期、优先级、按状态筛选）
- 旧 11 个用例全部保留，回归通过

---

## [v0.2.0] - 2026-06-14

### 重构
- 单体 main.py 拆分为 model / storage / service 三层
- task_model.py：数据模型
- task_storage.py：JSON 读写与容错
- task_service.py：业务逻辑
- main.py：命令行入口（从 150 行精简到 75 行）

---

## [v0.1.0] - 2026-06-14

### 首次发布
- 命令行任务管理：add / list / done
- JSON 数据持久化
- 用户故事与验收标准