"""
CampusTask v0.3.0 — 迭代开发
命令行入口，仅负责参数解析与输出，业务逻辑委托给 task_service
新增命令：search、overdue、add 支持 --deadline 和 --priority
用法：
  python main.py add "任务标题" [--deadline YYYY-MM-DD] [--priority high|medium|low]
  python main.py list [pending|done]
  python main.py done <编号>
  python main.py search <关键字>
  python main.py overdue
"""
import sys
from lab2.task_service import (
    add_new_task, get_all_tasks, mark_task_done,
    search_tasks, get_overdue_tasks, get_tasks_by_status
)


def print_help():
    """打印帮助信息"""
    print("""
╔══════════════════════════════════════════════════════╗
║           🎓 CampusTask v0.3.0  校园任务清单          ║
╠══════════════════════════════════════════════════════╣
║  用法:                                                ║
║    python main.py add "标题" [--deadline DATE]        ║
║                     [--priority high|medium|low]      ║
║    python main.py list [pending|done]   → 查看任务     ║
║    python main.py done <编号>           → 标记完成     ║
║    python main.py search <关键字>        → 搜索任务     ║
║    python main.py overdue               → 逾期任务     ║
╚══════════════════════════════════════════════════════╝
""")


def print_task_list(tasks):
    """格式化打印任务列表"""
    if not tasks:
        print("📭 暂无任务。")
        return
    print(f"\n{'='*60}")
    print(f"  📋 任务清单（共 {len(tasks)} 项）")
    print(f"{'='*60}")
    for t in tasks:
        icon = "✅" if t["status"] == "done" else "⏳"
        print(f"  [{t['id']}] {icon} {t['title']}")
        print(f"      状态: {t['status']}  |  "
              f"优先级: {t.get('priority','-')}  |  "
              f"截止: {t.get('deadline') or '无'}")
        print(f"      创建时间: {t['created_at']}")
    print(f"{'='*60}\n")


def main():
    """主函数：解析命令行参数并分发到业务层"""
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()

    # ---- add ----
    if command == "add":
        if len(sys.argv) < 3:
            print("❌ 错误：请提供任务标题。")
            return
        title = sys.argv[2]
        deadline = ""
        priority = "medium"
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--deadline" and i + 1 < len(sys.argv):
                deadline = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--priority" and i + 1 < len(sys.argv):
                priority = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        task = add_new_task(title, deadline, priority)
        print(f"✅ 任务已添加：[{task['id']}] {task['title']}"
              f"（优先级: {priority}" + (f"，截止: {deadline}" if deadline else "") + "）")

    # ---- list ----
    elif command == "list":
        filter_arg = sys.argv[2] if len(sys.argv) >= 3 else ""
        if filter_arg in ("pending", "done"):
            tasks = get_tasks_by_status(filter_arg)
        else:
            tasks = get_all_tasks()
        print_task_list(tasks)

    # ---- done ----
    elif command == "done":
        if len(sys.argv) < 3:
            print("❌ 错误：请提供任务编号。")
            return
        try:
            tid = int(sys.argv[2])
        except ValueError:
            print("❌ 错误：任务编号必须是整数。")
            return
        result = mark_task_done(tid)
        if result == "done":
            print(f"🎉 任务 [{tid}] 已标记为完成！")
        elif result == "already_done":
            print(f"⚠️  任务 [{tid}] 已经是完成状态。")
        else:
            print(f"❌ 错误：未找到编号为 {tid} 的任务。")

    # ---- search ----
    elif command == "search":
        if len(sys.argv) < 3:
            print("❌ 错误：请提供搜索关键字。")
            return
        results = search_tasks(sys.argv[2])
        print_task_list(results)

    # ---- overdue ----
    elif command == "overdue":
        overdue_tasks = get_overdue_tasks()
        print_task_list(overdue_tasks)

    # ---- unknown ----
    else:
        print(f"❌ 未知命令: {command}")
        print_help()


if __name__ == "__main__":
    main()