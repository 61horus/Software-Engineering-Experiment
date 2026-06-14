"""
任务业务逻辑层 —— 负责添加、查询、完成任务的核心业务
v0.3.0 新增：搜索关键字、显示逾期任务、按条件筛选
"""
from datetime import datetime
from campus_task.task_model import create_task, get_next_task_id
from campus_task.task_storage import load_tasks, save_tasks


def add_new_task(title: str, deadline: str = "", priority: str = "medium") -> dict:
    """添加新任务并持久化，返回创建的任务"""
    tasks = load_tasks()
    new_task = create_task(get_next_task_id(tasks), title, deadline, priority)
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task


def get_all_tasks() -> list:
    """获取所有任务"""
    return load_tasks()


def search_tasks(keyword: str) -> list:
    """按关键字搜索任务（匹配标题）"""
    tasks = load_tasks()
    kw = keyword.lower()
    return [t for t in tasks if kw in t["title"].lower()]


def get_overdue_tasks() -> list:
    """获取所有逾期任务（截止日期已过且状态为 pending）"""
    tasks = load_tasks()
    today = datetime.now().strftime("%Y-%m-%d")
    overdue = []
    for t in tasks:
        if t["status"] == "done":
            continue
        if t.get("deadline") and t["deadline"] < today:
            overdue.append(t)
    return overdue


def get_tasks_by_status(status: str) -> list:
    """按状态筛选任务（pending / done）"""
    tasks = load_tasks()
    return [t for t in tasks if t["status"] == status]


def export_to_csv(filepath: str) -> int:
    """导出所有任务为 CSV 文件，返回导出行数（不含表头）"""
    import csv
    tasks = load_tasks()
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "status", "deadline", "priority", "created_at"])
        writer.writeheader()
        for t in tasks:
            writer.writerow({
                "id": t["id"],
                "title": t["title"],
                "status": t["status"],
                "deadline": t.get("deadline", ""),
                "priority": t.get("priority", "medium"),
                "created_at": t["created_at"]
            })
    return len(tasks)


def mark_task_done(task_id: int) -> str:
    """
    将指定任务标记为完成。
    返回结果字符串：'done' / 'already_done' / 'not_found'
    """
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if task["status"] == "done":
                return "already_done"
            task["status"] = "done"
            save_tasks(tasks)
            return "done"
    return "not_found"