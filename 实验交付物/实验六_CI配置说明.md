# 实验六 — CI 配置说明

## 配置文件

- `pyproject.toml` — 项目元数据与 pytest 配置
- `.github/workflows/test.yml` — GitHub Actions 工作流

## 工作流内容

```yaml
name: Python Tests
on:
  push:
    branches: [master]
  pull_request:
    branches: [master]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install pytest
      - run: python -m pytest tests/ -v
```

## CI 流程

每次 push 到 master 或发起 PR 时，GitHub Actions 自动：
1. 检出代码
2. 安装 Python 3.11
3. 安装 pytest
4. 运行 16 个测试用例

## 失败-修复流程

| 步骤 | 操作 | CI 状态 |
|------|------|---------|
| 1 | 提交正常代码 | 🟢 绿灯（全部通过） |
| 2 | 引入 bug（如 tasks.remove 替代 status="done"） | 🔴 红灯（2个失败） |
| 3 | 修复 bug | 🟢 绿灯（恢复通过） |