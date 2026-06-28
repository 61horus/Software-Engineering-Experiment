# Software-Engineering-Experiment

软件工程实验（南昌航空大学）— CampusTask 校园任务清单

学号：24046523　姓名：陆一睿

---

## 项目简介

CampusTask 是一个命令行校园任务管理工具，支持添加、查看、完成、搜索、导出课程作业和实验报告等任务。数据以 JSON 格式持久化，程序重启不丢失。

**版本**：v0.5.0

## 仓库结构

```
campus_task/          # 主包
├── __init__.py       # 包标记
├── __main__.py       # python -m 入口
├── main.py           # CLI（argparse 子命令）
├── task_model.py     # 数据模型层（实验二）
├── task_storage.py   # JSON 存储层（实验二）
├── task_service.py   # 业务逻辑层（实验二/五）
├── ai_harness.py     # AI Harness（实验八）
├── eval_cases.json   # 评测用例（实验八）
├── trace.jsonl       # 追踪日志（实验八）
├── tasks.json        # 运行时数据
├── tasks_example.json
├── README.md         # 用户故事+验收标准（实验一）
├── CHANGELOG.md      # 版本说明（实验七）
└── USER_GUIDE.md     # 用户手册（实验七）

tests/                # pytest 测试（实验三）
├── __init__.py
└── test_campus_task.py

.github/workflows/    # CI（实验六）
└── test.yml

实验交付物/            # 各实验文档类交付物
├── 实验二_模块关系图.md
├── 实验三_需求与测试用例对应表.md
├── 实验五_变更请求表.md
├── 实验六_CI配置说明.md
├── 实验七_Bug报告与修复.md
└── 实验八_Harness架构图与反思.md

pyproject.toml        # 项目配置（实验六）
CHANGELOG.md          # 版本变更日志
实验报告规范.md        # 报告撰写规范
```

## 快速开始

```bash
# 安装（无需第三方依赖，Python 3.8+）
git clone git@gitee.com:horus61/Software-Engineering-Experiment.git
cd Software-Engineering-Experiment

# 添加任务
python -m campus_task add "复习软件工程" --deadline 2026-06-20 --priority high

# 查看所有任务
python -m campus_task list

# 查看待办
python -m campus_task list pending

# 标记完成
python -m campus_task done 1

# 搜索
python -m campus_task search 软件工程

# 逾期检测
python -m campus_task overdue

# 导出 CSV
python -m campus_task export tasks.csv

# 查看版本
python -m campus_task --version

# AI Harness（实验八）
python -m campus_task.ai_harness

# 运行测试
python -m pytest tests/ -v
```

## 实验对应关系

| 实验 | 内容 | 代码位置 | 文档位置 |
|------|------|----------|----------|
| 实验一 | 需求分析 & 最小可用产品 | `campus_task/main.py` (初始版) | `campus_task/README.md` |
| 实验二 | 模块化重构 | `campus_task/task_model.py` 等4文件 | `实验交付物/实验二_模块关系图.md` |
| 实验三 | pytest 测试 | `tests/test_campus_task.py` | `实验交付物/实验三_需求与测试用例对应表.md` |
| 实验四 | Git 协作与版本控制 | 全仓库 commit / branch / merge | `实验交付物/实验四_Git协作与版本控制.md` |
| 实验五 | 需求工程 & 迭代 | `campus_task/task_service.py` | `实验交付物/实验五_变更请求表.md` |
| 实验六 | CI/GitHub Actions | `.github/workflows/test.yml` | `实验交付物/实验六_CI配置说明.md` |
| 实验七 | 发布 & 运维 | `campus_task/main.py` (argparse版) | `实验交付物/实验七_Bug报告与修复.md` |
| 实验八 | AI Harness | `campus_task/ai_harness.py` | `实验交付物/实验八_Harness架构图与反思.md` |

## 技术栈

- Python 3.8+
- pytest（测试）
- ruff + mypy（代码质量）
- GitHub Actions（CI）
- 零外部依赖（标准库实现）

## 相关文档

- [用户手册](campus_task/USER_GUIDE.md)
- [变更日志](CHANGELOG.md)
- [项目说明（含用户故事）](campus_task/README.md)
