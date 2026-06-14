"""
任务存储层 —— 负责 JSON 文件的读写与容错
"""
import json
import os

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(DATA_DIR, "tasks.json")
EXAMPLE_FILE = os.path.join(DATA_DIR, "tasks_example.json")


def load_tasks() -> list:
    """读取任务列表，文件不存在时从示例初始化"""
    if not os.path.exists(DATA_FILE):
        _init_from_example()
    return _read_json_file()


def _init_from_example():
    """从示例文件复制初始数据"""
    if not os.path.exists(EXAMPLE_FILE):
        return
    try:
        with open(EXAMPLE_FILE, "r", encoding="utf-8") as src:
            content = src.read()
        with open(DATA_FILE, "w", encoding="utf-8") as dst:
            dst.write(content)
        print("📋 已从示例文件初始化任务数据。")
    except IOError:
        pass


def _read_json_file() -> list:
    """解析 JSON，含容错"""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            tasks = json.loads(content)
            return tasks if isinstance(tasks, list) else []
    except (json.JSONDecodeError, IOError):
        print("警告：数据文件损坏，已重置为空列表。")
        return []


def save_tasks(tasks: list) -> None:
    """写入 tasks.json"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)