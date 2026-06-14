# 实验七 — Bug 报告与修复

## Bug 报告

**标题**：当 tasks.json 为空文件时程序直接崩溃

**复现步骤**：
1. 手动创建空的 tasks.json 文件
2. 运行 python -m campus_task list
3. 观察：程序崩溃，抛出 JSONDecodeError

**根因**：早期版本 load_tasks() 未处理空文件场景，json.load("") 直接抛异常。

## 修复方案

在 _read_json_file() 中增加空内容检查：
```python
content = f.read().strip()
if not content:
    return []
```

## 验证

修复后提交，16/16 测试全部通过，CI 绿灯。

## 版本说明

v0.4.0 版本变更：
- argparse 替代 sys.argv
- 新增 --version 和 --help
- 错误日志写入 campus_task.log
- 用户手册 USER_GUIDE.md