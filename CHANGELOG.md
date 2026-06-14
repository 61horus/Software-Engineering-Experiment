# CHANGELOG

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