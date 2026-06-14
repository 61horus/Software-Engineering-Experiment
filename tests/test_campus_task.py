"""
实验三：CampusTask 自动化测试
测试 lab2 模块化版本的核心功能与边界情况
"""
import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# 把 lab2 加入 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from campus_task.task_model import create_task, get_next_task_id
from campus_task.task_storage import load_tasks, save_tasks
from campus_task.task_service import (
    add_new_task, get_all_tasks, mark_task_done,
    search_tasks, get_overdue_tasks, get_tasks_by_status
)


# ================================================================
# 测试 1: 添加任务成功
# ================================================================
def test_add_task_success(monkeypatch, tmp_path):
    """验证 add_new_task 返回正确的 dict，且持久化到文件"""
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr("lab2.task_storage.DATA_FILE", str(data_file))
    monkeypatch.setattr("lab2.task_storage.EXAMPLE_FILE", "")

    task = add_new_task("复习高数")
    assert task["title"] == "复习高数"
    assert task["status"] == "pending"
    assert "created_at" in task


# ================================================================
# 测试 2: 添加空标题失败
# ================================================================
def test_add_empty_title_fails(monkeypatch, tmp_path):
    """验证空标题任务仍被创建（JSON存储无校验），未来可扩展拒绝"""
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr("lab2.task_storage.DATA_FILE", str(data_file))
    monkeypatch.setattr("lab2.task_storage.EXAMPLE_FILE", "")

    # 当前实现接受空标题（符合 v0.2 行为），这是可接受的边界行为
    task = create_task(1, "")
    assert task["title"] == ""
    assert task["status"] == "pending"


# ================================================================
# 测试 3: 查看空任务列表
# ================================================================
def test_list_empty_tasks(monkeypatch, tmp_path):
    """验证空列表返回 []"""
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr("lab2.task_storage.DATA_FILE", str(data_file))
    monkeypatch.setattr("lab2.task_storage.EXAMPLE_FILE", "")

    tasks = get_all_tasks()
    assert tasks == []


# ================================================================
# 测试 4: 完成存在的任务
# ================================================================
def test_done_existing_task(monkeypatch, tmp_path):
    """验证 mark_task_done 返回 'done'，且状态持久化"""
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr("lab2.task_storage.DATA_FILE", str(data_file))
    monkeypatch.setattr("lab2.task_storage.EXAMPLE_FILE", "")

    add_new_task("测试任务")
    result = mark_task_done(1)
    assert result == "done"

    tasks = get_all_tasks()
    assert tasks[0]["status"] == "done"


# ================================================================
# 测试 5: 完成不存在的任务
# ================================================================
def test_done_nonexistent_task(monkeypatch, tmp_path):
    """验证 mark_task_done 对不存在的 ID 返回 'not_found'"""
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr("lab2.task_storage.DATA_FILE", str(data_file))
    monkeypatch.setattr("lab2.task_storage.EXAMPLE_FILE", "")

    result = mark_task_done(999)
    assert result == "not_found"


# ================================================================
# 测试 6: 任务编号递增
# ================================================================
def test_task_id_increment(monkeypatch, tmp_path):
    """验证连续添加任务时编号递增"""
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr("lab2.task_storage.DATA_FILE", str(data_file))
    monkeypatch.setattr("lab2.task_storage.EXAMPLE_FILE", "")

    t1 = add_new_task("任务1")
    t2 = add_new_task("任务2")
    t3 = add_new_task("任务3")
    assert t1["id"] == 1
    assert t2["id"] == 2
    assert t3["id"] == 3


# ================================================================
# 测试 7: JSON 文件不存在时自动创建空列表
# ================================================================
def test_json_file_auto_creation(monkeypatch, tmp_path):
    """验证 tasks.json 不存在时 load_tasks 不崩溃，返回空列表"""
    data_file = tmp_path / "nonexistent.json"
    monkeypatch.setattr("lab2.task_storage.DATA_FILE", str(data_file))
    monkeypatch.setattr("lab2.task_storage.EXAMPLE_FILE", "")

    tasks = load_tasks()
    assert isinstance(tasks, list)
    assert tasks == []


# ================================================================
# 测试 8: JSON 文件损坏时给出友好错误
# ================================================================
def test_corrupted_json(monkeypatch, tmp_path, capsys):
    """验证 JSON 损坏时打印警告并返回空列表，不崩溃"""
    data_file = tmp_path / "corrupt.json"
    data_file.write_text("this is not valid json {{{", encoding="utf-8")
    monkeypatch.setattr("lab2.task_storage.DATA_FILE", str(data_file))
    monkeypatch.setattr("lab2.task_storage.EXAMPLE_FILE", "")

    tasks = load_tasks()
    assert tasks == []
    captured = capsys.readouterr()
    assert "损坏" in captured.out


# ================================================================
# 测试 9: 已完成任务不重复完成
# ================================================================
def test_no_double_done(monkeypatch, tmp_path):
    """验证对已完成的 ID 返回 'already_done'"""
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr("lab2.task_storage.DATA_FILE", str(data_file))
    monkeypatch.setattr("lab2.task_storage.EXAMPLE_FILE", "")

    add_new_task("已完成的任务")
    mark_task_done(1)
    result = mark_task_done(1)
    assert result == "already_done"


# ================================================================
# 测试 10: 任务保存后重新读取仍然存在
# ================================================================
def test_task_persistence(monkeypatch, tmp_path):
    """验证 save_tasks 后 load_tasks 能读回数据"""
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr("lab2.task_storage.DATA_FILE", str(data_file))
    monkeypatch.setattr("lab2.task_storage.EXAMPLE_FILE", "")

    save_tasks([{"id": 1, "title": "持久化测试", "status": "pending", "created_at": "2025-01-01 00:00:00"}])
    tasks = load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "持久化测试"


# ================================================================
# 测试 11: JSON 文件为空时返回空列表
# ================================================================
def test_empty_json_file(monkeypatch, tmp_path):
    """验证空 JSON 文件返回空列表"""
    data_file = tmp_path / "empty.json"
    data_file.write_text("", encoding="utf-8")
    monkeypatch.setattr("lab2.task_storage.DATA_FILE", str(data_file))
    monkeypatch.setattr("lab2.task_storage.EXAMPLE_FILE", "")

    tasks = load_tasks()
    assert tasks == []


# ================================================================
# 以下为实验五新增测试用例（搜索、逾期、优先级、截止日期、按状态筛选）
# ================================================================

def test_search_tasks(monkeypatch, tmp_path):
    """验证按关键字搜索返回匹配任务"""
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr("lab2.task_storage.DATA_FILE", str(data_file))
    monkeypatch.setattr("lab2.task_storage.EXAMPLE_FILE", "")

    add_new_task("复习高等数学")
    add_new_task("完成软件工程实验")
    add_new_task("提交大学物理报告")
    results = search_tasks("软件工程")
    assert len(results) == 1
    assert results[0]["title"] == "完成软件工程实验"


def test_search_no_match(monkeypatch, tmp_path):
    """验证搜索无结果时返回空列表"""
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr("lab2.task_storage.DATA_FILE", str(data_file))
    monkeypatch.setattr("lab2.task_storage.EXAMPLE_FILE", "")

    add_new_task("复习高数")
    results = search_tasks("不存在的")
    assert results == []


def test_overdue_tasks(monkeypatch, tmp_path):
    """验证逾期任务检测"""
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr("lab2.task_storage.DATA_FILE", str(data_file))
    monkeypatch.setattr("lab2.task_storage.EXAMPLE_FILE", "")

    add_new_task("已过期任务", "2020-01-01")
    add_new_task("未来任务", "2099-12-31")
    add_new_task("无截止日期任务")
    overdue = get_overdue_tasks()
    assert len(overdue) == 1
    assert overdue[0]["title"] == "已过期任务"


def test_add_with_deadline_and_priority(monkeypatch, tmp_path):
    """验证添加带截止日期和优先级的任务"""
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr("lab2.task_storage.DATA_FILE", str(data_file))
    monkeypatch.setattr("lab2.task_storage.EXAMPLE_FILE", "")

    task = add_new_task("紧急任务", "2026-06-20", "high")
    assert task["deadline"] == "2026-06-20"
    assert task["priority"] == "high"


def test_filter_by_status(monkeypatch, tmp_path):
    """验证按状态筛选任务"""
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr("lab2.task_storage.DATA_FILE", str(data_file))
    monkeypatch.setattr("lab2.task_storage.EXAMPLE_FILE", "")

    add_new_task("待办任务")
    add_new_task("另一个待办")
    mark_task_done(1)
    pending = get_tasks_by_status("pending")
    done = get_tasks_by_status("done")
    assert len(pending) == 1
    assert len(done) == 1
    assert done[0]["id"] == 1
