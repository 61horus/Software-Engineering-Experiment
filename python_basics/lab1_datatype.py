# 数据类型探索 - 实验一 任务3
# 学号：24046523 姓名：陆一睿

print("=" * 40)
print("任务3：数据类型探索 - 序列类型")
print("=" * 40)

# ============================================
# 1. 列表操作
# ============================================
print("\n--- 1. 列表操作 ---")
languages = ["Python", "Java", "C++"]
print(f"原始列表: {languages}")
# 修改列表中的元素（列表是可变的）
languages[1] = "JavaScript"
print(f"修改后的列表: {languages}")
# 追加元素
languages.append("Go")
print(f"追加后的列表: {languages}")

# ============================================
# 2. 元组操作（尝试修改会报错）
# ============================================
print("\n--- 2. 元组操作 ---")
versions = (3.8, 3.9, 3.10)
print(f"元组内容: {versions}")
print(f"元组类型: {type(versions)}")

# 故意尝试修改元组，捕获错误
print("尝试修改元组 versions[0] = 3.11 ...")
try:
    versions[0] = 3.11  # 这行会触发 TypeError
    print("修改成功（不应该执行到这里）")
except TypeError as e:
    print(f"元组修改错误: {e}")
    print("结论：元组是不可变类型，不能修改元素")

# 元组的正确用法：解包
v1, v2, v3 = versions
print(f"元组解包: v1={v1}, v2={v2}, v3={v3}")

# ============================================
# 3. 字典操作
# ============================================
print("\n--- 3. 字典操作 ---")
student = {"name": "李华", "id": 20230101}
print(f"原始字典: {student}")
# 添加新键值对
student["major"] = "计算机科学"
print(f"添加major后: {student}")
# 修改已有键的值
student["id"] = 24046523
print(f"修改id后: {student}")
# 访问字典元素
print(f"学生姓名: {student['name']}")
print(f"学生专业: {student.get('major', '未设置')}")
print(f"学生班级: {student.get('class', '未设置（默认值）')}")

# ============================================
# 4. 集合操作 - 去重演示
# ============================================
print("\n--- 4. 集合操作 ---")
# 集合自动去重
numbers = {1, 2, 2, 3, 3, 3}
print(f"原始输入: {{1, 2, 2, 3, 3, 3}}")
print(f"去重结果: {numbers}")
print(f"集合类型: {type(numbers)}")

# 集合运算
set_a = {1, 2, 3, 4}
set_b = {3, 4, 5, 6}
print(f"\n集合A: {set_a}")
print(f"集合B: {set_b}")
print(f"并集 A|B: {set_a | set_b}")
print(f"交集 A&B: {set_a & set_b}")
print(f"差集 A-B: {set_a - set_b}")

# ============================================
# 5. 输出验证
# ============================================
print("\n--- 5. 输出验证 ---")
# 验证1：列表元素类型可以混合
test_list = [1, "a", 3.14]
type_list = [type(item) for item in test_list]
print(f"验证1 - 列表元素类型检测: {type_list}")

# 验证2：字典键必须是不可变类型
print("验证2 - 字典键类型测试:")
try:
    bad_dict = {[1, 2]: "value"}  # 列表是可变的，不能做键
except TypeError as e:
    print(f"  列表作为字典键错误: {e}")

# 验证3：集合不能包含可变元素
print("验证3 - 集合元素测试:")
try:
    bad_set = {[1, 2], 3}  # 列表不能放入集合
except TypeError as e:
    print(f"  列表放入集合错误: {e}")