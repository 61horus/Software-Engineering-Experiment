# CHANGELOG

## [v0.4.0] - 2026-06-14

### 新增 & 变更
- argparse 子命令替代 sys.argv 解析，支持 --help 和 --version
- 错误日志记录到 campus_task.log
- 使用方式改为 python -m campus_task <命令>

---

## [v0.3.0] - 2026-06-14

### 新增功能
- search <关键字> 按标题搜索任务
- overdue 命令显示逾期任务
- add 支持 --deadline 和 --priority 标志
- list 支持 pending/done 状态筛选

---

## [v0.2.0] - 2026-06-14

### 重构
- 单体 main.py 拆分为 model / storage / service 三层

---

## [v0.1.0] - 2026-06-14

### 首次发布
- 命令行任务管理：add / list / done
- JSON 数据持久化
- 用户故事与验收标准