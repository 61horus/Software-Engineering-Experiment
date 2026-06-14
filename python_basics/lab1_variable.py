# 变量操作实验 - 实验一 任务2
# 学号：24046523 姓名：陆一睿

print("=" * 40)
print("任务2：变量操作实验")
print("=" * 40)

# ============================================
# 1. 多变量赋值与类型检测
# ============================================
print("\n--- 1. 多变量赋值 ---")
a, b, c = 10, 3.14, "Python"
print(f"整型: {a} 类型: {type(a)}")
print(f"浮点型: {b} 类型: {type(b)}")
print(f"字符串: {c} 类型: {type(c)}")

# ============================================
# 2. 强制类型转换
# ============================================
print("\n--- 2. 强制类型转换 ---")
num_str = "123"
num_int = int(num_str)
print(f"转换前: '{num_str}' 类型: {type(num_str)}")
print(f"转换后: {num_int} 类型: {type(num_int)}")

# 更多类型转换演示
# 整型转浮点
int_val = 42
float_val = float(int_val)
print(f"整型 {int_val} -> 浮点型 {float_val} 类型: {type(float_val)}")

# 浮点转整型（注意截断）
pi = 3.14159
pi_int = int(pi)
print(f"浮点 {pi} -> 整型 {pi_int}（小数部分被截断）类型: {type(pi_int)}")

# 数值转字符串
num = 2024
num_to_str = str(num)
print(f"整型 {num} -> 字符串 '{num_to_str}' 类型: {type(num_to_str)}")

# ============================================
# 3. 输出验证（至少3个）
# ============================================
print("\n--- 3. 输出验证 ---")
# 验证1：检查类型转换是否会失败
try:
    invalid_str = "abc123"
    converted = int(invalid_str)
except ValueError as e:
    print(f"验证1 - 非法字符串转换错误: {e}")

# 验证2：验证Python是动态类型语言
dynamic_var = 100
print(f"验证2 - dynamic_var 当前值: {dynamic_var} 类型: {type(dynamic_var)}")
dynamic_var = "现在是字符串"
print(f"验证2 - dynamic_var 新值: {dynamic_var} 类型: {type(dynamic_var)}")

# 验证3：验证变量内存地址（id）
x = 10
y = 10  # Python小整数缓存
z = 999
w = 999
print(f"验证3 - x(10) id: {id(x)}, y(10) id: {id(y)} （相同，小整数缓存）")
print(f"验证3 - z(999) id: {id(z)}, w(999) id: {id(w)} （可能不同）")