"""
CampusTask v0.2.0 — 模块化重构
命令行入口，仅负责参数解析与输出，业务逻辑委托给 task_service
用法：
  python main.py add "任务标题"
  python main.py list
  python main.py done <任务编号>
"""
import sys
from campus_task.task_service import add_new_task, get_all_tasks, mark_task_done


def print_help():
    """打印帮助信息"""
    print("""
╔══════════════════════════════════════════╗
║         🎓 CampusTask 校园任务清单        ║
╠══════════════════════════════════════════╣
║  用法:                                    ║
║    python main.py add "任务标题"   → 添加 ║
║    python main.py list              → 查看 ║
║    python main.py done <编号>       → 完成 ║
╚══════════════════════════════════════════╝
""")


def main():
    """主函数：解析命令行参数并分发到业务层"""
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 3:
            print("❌ 错误：请提供任务标题。")
            return
        task = add_new_task(sys.argv[2])
        print(f"✅ 任务已添加：[{task['id']}] {task['title']}")

    elif command == "list":
        tasks = get_all_tasks()
        if not tasks:
            print("📭 暂无任务。")
            return
        print(f"\n{'='*50}")
        print(f"  📋 任务清单（共 {len(tasks)} 项）")
        print(f"{'='*50}")
        for t in tasks:
            icon = "✅" if t["status"] == "done" else "⏳"
            print(f"  [{t['id']}] {icon} {t['title']}")
            print(f"      创建时间: {t['created_at']}  状态: {t['status']}")
        print(f"{'='*50}\n")

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

    else:
        print(f"❌ 未知命令: {command}")
        print_help()


if __name__ == "__main__":
    main()