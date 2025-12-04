# Omnidiff 项目介绍
![omnidiff](https://github.com/game1024/omnidiff/blob/main/images/omnidiff.jpg)

## 一、项目概述
Omnidiff 是一个用于比较两个 JSON 对象差异的 Python 库。它能够深入分析两个 JSON 对象，找出它们之间的不同字段、在一个对象中存在而另一个对象中缺失的字段。此外，项目还提供了对 JSON 对象进行路径映射、根据通配路径匹配等功能，支持跳过指定路径的比较，提高了比较的灵活性和效率。

## 二、功能特性
1. **JSON 对象比较**：可以精确比较两个 JSON 对象，找出差异字段、一方缺失的字段。
2. **通配路径匹配**：支持使用通配符（如 `*`）来定义路径，方便进行模糊匹配。
3. **路径跳过功能**：在比较过程中，可以指定跳过某些路径，避免不必要的比较。
4. **JSON 对象映射**：可以根据指定的映射路径和哈希函数对 JSON 对象进行映射转换。
5. **性能监测**：使用装饰器对函数执行时间进行监测，方便性能优化。

## 三、安装与依赖
### 安装
你可以使用以下命令安装 `omnidiff`：
```bash
pip install omnidiff
```

### 依赖
该项目依赖以下 Python 库：
- `copy`：用于深拷贝 JSON 对象。
- `re`：用于正则表达式匹配，处理通配路径。
- `time`：用于函数执行时间监测。
- `jmespath`：用于从 JSON 对象中提取指定路径的值。



## 四、使用示例

### 1. 比较两个 JSON 对象
```python
import json
from omnidiff import compare, CompareResult

a_json = {
    "name": "Alice",
    "age": 25,
    "hobbies": ["reading", "swimming"]
}

b_json = {
    "name": "Bob",
    "age": 30,
    "hobbies": ["running", "swimming"]
}

result = compare(a_json, b_json)
print("不同字段：", result.diff_fields)
print("A 中缺失的字段：", result.a_missing_fields)
print("B 中缺失的字段：", result.b_missing_fields)
```

### 2. 跳过指定路径的比较
```python
skip_paths = ["age"]
result = compare(a_json, b_json, skip_paths)
```

### 3. JSON 对象映射
```python
from omnidiff import map_jmespath

def hash_func(node):
    return str(hash(node))

json_obj = ["apple", "banana", "cherry"]
mapped_obj = map_jmespath(json_obj, "@", hash_func)
print(mapped_obj)
```

## 五、代码结构
### 主要函数和类
1. **`compare` 函数**：比较两个 JSON 对象，返回 `CompareResult` 类的实例，包含差异字段、一方缺失的字段信息。
2. **`match_wildcard` 函数**：判断路径是否与通配路径匹配。
3. **`map_jmespath` 函数**：根据指定的映射路径和哈希函数对 JSON 对象进行映射转换。
4. **`get_jmespath` 函数**：获取 JSON 对象中所有路径的列表，可以跳过指定路径。
5. **`CompareResult` 类**：用于存储比较结果，包含 `diff_fields`（差异字段）、`a_missing_fields`（A 中缺失的字段）、`b_missing_fields`（B 中缺失的字段）。

## 六、注意事项
- 在使用 `compare` 函数时，确保输入的是有效的 JSON 对象。
- 对于通配路径，使用 `*` 作为通配符，目前仅支持匹配数字。
- 当使用 `map_jmespath` 函数时，确保哈希函数 `hash_func` 能够正确处理 JSON 对象中的元素。

## 七、贡献与反馈
如果你发现项目存在问题或有改进建议，欢迎提交 Issues 或 Pull Requests。同时，也欢迎你参与项目的开发和维护，共同完善 Omnidiff 项目。

