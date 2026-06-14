# CampusTask 用户手册 (v0.4.0)

## 快速开始

```bash
# 添加任务
python -m campus_task add "复习软件工程" --deadline 2026-06-20 --priority high

# 查看所有任务
python -m campus_task list

# 查看待办任务
python -m campus_task list pending

# 标记完成
python -m campus_task done 1

# 搜索任务
python -m campus_task search 软件工程

# 查看逾期任务
python -m campus_task overdue

# 查看版本
python -m campus_task --version
```

## 命令参考

| 命令 | 说明 | 参数 |
|------|------|------|
| add | 添加任务 | title, --deadline, --priority |
| list | 列出任务 | [pending/done] |
| done | 标记完成 | task_id |
| search | 搜索任务 | keyword |
| overdue | 逾期任务 | 无 |

## 数据文件

任务数据保存在 `campus_task/tasks.json`，首次运行自动从示例文件初始化。

## 错误日志

错误记录在 `campus_task/campus_task.log`。