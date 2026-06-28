"""
CampusTask v0.4.0 — 可发布命令行工具
支持 argparse、--version、错误日志、CSV导出
用法：
  python -m campus_task add "任务标题" [--deadline DATE] [--priority high|medium|low]
  python -m campus_task list [pending|done]
  python -m campus_task done <编号>
  python -m campus_task search <关键字>
  python -m campus_task overdue
  python -m campus_task export <文件路径.csv>
  python -m campus_task --version
"""
import argparse
import logging
import os
import sys

# 日志配置：写入 campus_task.log
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "campus_task.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

from campus_task.task_service import (
    add_new_task, get_all_tasks, mark_task_done,
    search_tasks, get_overdue_tasks, get_tasks_by_status,
    export_to_csv
)

VERSION = "0.4.0"


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
              f"分类: {t.get('category','-')}  |  "
              f"截止: {t.get('deadline') or '无'}")
        print(f"      创建时间: {t['created_at']}")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="CampusTask - 校园任务清单 (v%s)" % VERSION,
        prog="campus_task"
    )
    parser.add_argument("--version", action="version", version="CampusTask v%s" % VERSION)

    sub = parser.add_subparsers(dest="command")

    # add
    p_add = sub.add_parser("add", help="添加任务")
    p_add.add_argument("title", help="任务标题")
    p_add.add_argument("--deadline", default="", help="截止日期 YYYY-MM-DD")
    p_add.add_argument("--priority", default="medium", choices=["high", "medium", "low"], help="优先级")
    p_add.add_argument("--category", default="general",
                       choices=["general", "作业", "实验", "考试", "其他"], help="任务分类")

    # list
    p_list = sub.add_parser("list", help="列出任务")
    p_list.add_argument("status", nargs="?", choices=["pending", "done"], help="筛选状态")

    # done
    p_done = sub.add_parser("done", help="标记完成")
    p_done.add_argument("task_id", type=int, help="任务编号")

    # search
    p_search = sub.add_parser("search", help="搜索任务")
    p_search.add_argument("keyword", help="关键字")

    # overdue
    sub.add_parser("overdue", help="逾期任务")

    # export
    p_export = sub.add_parser("export", help="导出CSV")
    p_export.add_argument("filepath", help="导出文件路径（如 tasks.csv）")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    try:
        if args.command == "add":
            task = add_new_task(args.title, args.deadline, args.priority, args.category)
            print(f"✅ 任务已添加：[{task['id']}] {task['title']}")
            logging.info(f"add task [{task['id']}] {task['title']}")

        elif args.command == "list":
            if args.status:
                tasks = get_tasks_by_status(args.status)
            else:
                tasks = get_all_tasks()
            print_task_list(tasks)

        elif args.command == "done":
            result = mark_task_done(args.task_id)
            if result == "done":
                print(f"🎉 任务 [{args.task_id}] 已标记为完成！")
                logging.info(f"done task [{args.task_id}]")
            elif result == "already_done":
                print(f"⚠️  任务 [{args.task_id}] 已经是完成状态。")
            else:
                print(f"❌ 错误：未找到编号为 {args.task_id} 的任务。")

        elif args.command == "search":
            results = search_tasks(args.keyword)
            print_task_list(results)

        elif args.command == "overdue":
            overdue_tasks = get_overdue_tasks()
            print_task_list(overdue_tasks)

        elif args.command == "export":
            count = export_to_csv(args.filepath)
            print(f"📊 已导出 {count} 条任务到 {args.filepath}")
            logging.info(f"export {count} tasks to {args.filepath}")

    except Exception as e:
        logging.error(f"执行命令 {args.command} 时出错: {e}")
        print(f"❌ 发生错误，详情见 campus_task.log")
        raise


if __name__ == "__main__":
    main()