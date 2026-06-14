"""
CampusTask AI Harness (实验八)
用自然语言管理任务 —— mock_model 模拟 AI 输出
核心流程：用户输入 → prompt_builder → mock_model → parser → guardrail → tool_executor
"""
import json
import os
from datetime import datetime
from campus_task.task_service import add_new_task, get_all_tasks, mark_task_done


def prompt_builder(user_input: str, task_state: dict) -> str:
    """构造 AI 提示，包含当前任务上下文"""
    return f"用户输入: {user_input}\n当前任务状态: {json.dumps(task_state, ensure_ascii=False)}\n请决定操作。"


def mock_model(prompt: str) -> dict:
    """模拟 AI 输出：简单规则匹配生成意图"""
    text = prompt.lower()
    if "添加" in text or "加一个" in text:
        return {"action": "add_task", "args": {"title": "软件工程实验报告", "deadline": "", "priority": "medium"}}
    elif "列出" in text or "还有什么" in text or "还没完成" in text:
        return {"action": "list_tasks", "args": {}}
    elif "标记" in text or "完成" in text:
        return {"action": "done_task", "args": {"task_id": 2}}
    elif "删除所有" in text:
        return {"action": "delete_all", "args": {}}
    return {"action": "unknown", "args": {}}


def parse_model_output(model_output: dict) -> dict:
    """直接返回模型输出（已为标准字典格式）"""
    return model_output


def guardrail(action: dict) -> (bool, str):
    """
    安全检查：高风险操作需要人工确认。
    返回：(通过, 消息)
    """
    if action.get("action") == "delete_all":
        return False, "删除所有任务需要人工确认，已拒绝执行。"
    return True, "OK"


def execute_tool(action: dict) -> str:
    """执行安全操作，调用 CampusTask 功能"""
    act = action["action"]
    args = action.get("args", {})
    if act == "add_task":
        t = add_new_task(args.get("title", "未命名任务"), args.get("deadline", ""), args.get("priority", "medium"))
        return f"已添加任务 [{t['id']}] {t['title']}"
    elif act == "list_tasks":
        tasks = get_all_tasks()
        pending = [t for t in tasks if t["status"] == "pending"]
        return f"还有 {len(pending)} 个待办任务: {[t['title'] for t in pending]}"
    elif act == "done_task":
        result = mark_task_done(args["task_id"])
        return "已完成" if result == "done" else "操作失败"
    return "未知操作"


def write_trace(event: dict):
    """写入 JSONL 跟踪日志"""
    trace_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trace.jsonl")
    event["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(trace_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def run_eval(eval_cases: list) -> float:
    """运行评测，返回准确率"""
    passed = 0
    for case in eval_cases:
        prompt = prompt_builder(case["input"], {})
        model_out = mock_model(prompt)
        parsed = parse_model_output(model_out)
        ok, _ = guardrail(parsed)
        if ok and parsed["action"] == case["expected_action"]:
            passed += 1
    return passed / len(eval_cases) if eval_cases else 0


def main():
    """交互式 AI Harness 入口"""
    print("═ CampusTask AI Harness (实验八) ═")
    while True:
        user_input = input("\n>>> ").strip()
        if not user_input:
            break
        prompt = prompt_builder(user_input, {})
        model_out = mock_model(prompt)
        parsed = parse_model_output(model_out)
        ok, msg = guardrail(parsed)
        write_trace({"input": user_input, "prompt": prompt, "model_output": model_out, "parsed": parsed, "guardrail_ok": ok})
        if not ok:
            print(f"⚠️ {msg}")
            continue
        result = execute_tool(parsed)
        print(result)


if __name__ == "__main__":
    main()