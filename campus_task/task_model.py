"""
任务数据模型层
定义 Task 数据结构及其创建工厂函数
"""
from datetime import datetime


def create_task(task_id: int, title: str, deadline: str = "", priority: str = "medium",
                tags: str = "", category: str = "general") -> dict:
    """创建一个新任务字典（状态默认为 pending，支持截止日期、优先级、标签和分类）"""
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    return {
        "id": task_id,
        "title": title,
        "status": "pending",
        "deadline": deadline,       # 格式 YYYY-MM-DD，空字符串表示无截止日期
        "priority": priority,       # high / medium / low
        "tags": tag_list,           # 标签列表，如 ["软件工程","作业"]
        "category": category,       # 任务分类：general / 作业 / 实验 / 考试 / 其他
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def get_next_task_id(tasks: list) -> int:
    """根据现有任务列表计算下一个可用编号"""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1
