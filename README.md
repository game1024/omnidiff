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

## 三、安装
### 安装
你可以使用以下命令安装 `omnidiff`：
```bash
pip install omnidiff
```


## 四、使用示例

### 1. 比较两个 JSON 对象
```python
import json
from omnidiff import compare
import pprint

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
pprint.pprint(result.diff_fields, width=60, sort_dicts=False)
'''
输出如下，结果是一个列表，其中包含了有差异的字段路径，a中的值，b中的值，和差异原因
[('@.age',
  25,
  30,
  'path:@.age is different, a_value:25 b_value:30'),
 ('@.hobbies[0]',
  'reading',
  'running',
  'path:@.hobbies[0] is different, a_value:reading '
  'b_value:running'),
 ('@.name',
  'Alice',
  'Bob',
  'path:@.name is different, a_value:Alice b_value:Bob')]
'''
```

### 2. 跳过指定路径的比较
如果需要忽略某个字段的比较，可以使用compare的第三个参数skip_paths
```python
import json
from omnidiff import compare
import pprint
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


skip_paths = ["@.age"] # 忽略@.age的字段比较
result = compare(a_json, b_json, skip_paths)
pprint.pprint(result.diff_fields, width=60, sort_dicts=False)

'''
输出如下，会返回结果中不会出现@.age的差异
[('@.hobbies[0]',
  'reading',
  'running',
  'path:@.hobbies[0] is different, a_value:reading '
  'b_value:running'),
 ('@.name',
  'Alice',
  'Bob',
  'path:@.name is different, a_value:Alice b_value:Bob')]
'''
```

### 3. JSON 对象映射
如果想要在比较前，对对象进行预处理，把其中的列表类型字段转化成字典类型，可以使用map_jmespath，该函数接受待转化的字段路径，和哈希转化函数


```python
from omnidiff import map_jmespath
import pprint

def hash_func(node):
    return str(hash(node))

json_obj = ["apple", "banana", "cherry"]


# 我们想将@路径的，直接转化成字典类型，key为hash_func的返回值，value为原数组元素的值
mapped_obj = map_jmespath(json_obj, "@", hash_func)

pprint.pprint(mapped_obj, width=60, sort_dicts=False)

'''
输出如下
{'7748484625998085887': 'apple',
 '1198650295607495188': 'banana',
 '7490853343013369096': 'cherry'}
'''
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

