# 高级数据类型实践 - 实验一 任务4
# 学号：24046523 姓名：陆一睿

print("=" * 40)
print("任务4：高级数据类型实践 - 字节与内存操作")
print("=" * 40)

# ============================================
# 1. 字节类型操作
# ============================================
print("\n--- 1. 字节类型 bytes ---")
# 使用ASCII码创建字节：H=72, e=101, l=108, l=108, o=111
byte_data = bytes([72, 101, 108, 108, 111])
print(f"字节数据(bytes): {byte_data}")
print(f"字节类型: {type(byte_data)}")
print(f"字节解码为字符串: {byte_data.decode('ascii')}")

# 从字符串创建字节
str_bytes = b"Hello Python"
print(f"\n字符串字面量创建字节: {str_bytes}")
print(f"字节长度: {len(str_bytes)} 字节")
print(f"单个字节访问: str_bytes[0] = {str_bytes[0]} (= 'H')")

# bytearray - 可变的字节序列
print("\n--- 2. 可变字节序列 bytearray ---")
arr = bytearray(b"Hello")
print(f"原始 bytearray: {arr}")
# 修改bytearray中的元素
arr[0] = 74  # 'J' 的 ASCII 码
print(f"修改后 bytearray: {arr}")
print(f"解码: {arr.decode('ascii')}")

# 追加字节
arr.append(33)  # '!' 的 ASCII 码
print(f"追加后 bytearray: {arr} ({arr.decode('ascii')})")

# ============================================
# 2. 内存视图演示
# ============================================
print("\n--- 3. 内存视图 memoryview ---")
# 创建bytearray并用memoryview查看
data = bytearray(b"Hello")
mem_view = memoryview(data)
print(f"内存视图对象: {mem_view}")
print(f"内存视图的原始对象(obj): {mem_view.obj}")
print(f"内存视图长度: {mem_view.nbytes} 字节")
print(f"内存视图格式: {mem_view.format}")
print(f"内存视图元素大小: {mem_view.itemsize} 字节")

# 通过内存视图读取
print(f"\n通过内存视图读取元素:")
for i in range(len(mem_view)):
    char = chr(mem_view[i])
    print(f"  mem_view[{i}] = {mem_view[i]} (字符: '{char}')")

# 通过内存视图修改底层数据
print("\n内存视图修改演示:")
print(f"修改前 data: {data}")
mem_view[0] = 74  # 改为 'J'
print(f"修改 mem_view[0] = 74 ('J') 后 data: {data}")
print("说明：memoryview修改会直接反映到底层bytearray")

# 内存视图切片
print("\n内存视图切片:")
slice_view = mem_view[1:4]
print(f"mem_view[1:4] = {slice_view} ({bytes(slice_view).decode('ascii')})")

# ============================================
# 3. 输出验证
# ============================================
print("\n--- 4. 输出验证 ---")
# 验证1：bytes是不可变的
print("验证1 - bytes不可变性测试:")
try:
    byte_data[0] = 65  # 尝试修改
except TypeError as e:
    print(f"  bytes修改错误: {e}")

# 验证2：bytearray是可变的
print("验证2 - bytearray可变性测试:")
ba = bytearray(b"Test")
print(f"  原始: {ba}")
ba[2] = ord('x')
print(f"  修改 ba[2]='x' 后: {ba}")
print(f"  bytearray可修改，与bytes不同")

# 验证3：memoryview零拷贝特性
print("验证3 - memoryview零拷贝验证:")
source = bytearray(b"ABCDEFG")
mv = memoryview(source)
# 修改memoryview子视图，验证底层数据同步变化
mv_sub = mv[2:5]
print(f"  原始 source: {source}")
mv_sub[0] = ord('X')
print(f"  修改 mv[2:5][0] = 'X' 后 source: {source}")
print(f"  说明：memoryview是零拷贝视图，直接操作底层内存")