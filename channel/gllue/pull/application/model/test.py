class MyClass:
    def __init__(self, value):
        self._my_attr = value

    @property
    def my_attr(self):
        return self._my_attr

# 创建对象并设置属性
obj = MyClass(10)

# 通过属性访问
print(obj._my_attr)  # 输出: 10

# 尝试修改属性（会抛出 AttributeError）
try:
    obj._my_attr = 20
except AttributeError as e:
    print("AttributeError:", e)
