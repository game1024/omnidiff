import copy
import re
import time

import jmespath

def path_exists(path):
    return True

def compare(json_obj1, json_obj2):
    if isinstance(json_obj1, dict) and isinstance(json_obj2, dict):
        pass

def is_dict(obj) -> bool:
    return type(obj) is dict

def is_list(obj) -> bool:
    return type(obj) is list

# 与通配路径的匹配
def match_wildcard(path, wildcard_path):
    def match_helper(node, wildcard_node):
        if wildcard_node == '*':
            return True
        elif wildcard_node.find('*') != -1:
            regex = re.escape(wildcard_node).replace(r'\*', r'\d+')
            pattern = re.compile(regex)
            result = bool(pattern.match(node))
            return result
        else:
            return node == wildcard_node

    path = path.split(".")
    wildcard_path = wildcard_path.split(".")
    if len(path) != len(wildcard_path):
        return False

    for node, wildcard_node in zip(path, wildcard_path):
        if not match_helper(node, wildcard_node):
            return False

    return True

def map_jmespath(json_obj, map_path, hash_func):
    json_obj = copy.deepcopy(json_obj)
    map_path = '' if map_path is None else map_path

    if '@' == map_path:
        json_obj = {hash_func(node): node for node in json_obj}

    _map_jmespath('@', json_obj, '@', None, map_path, hash_func)
    return json_obj

def _map_jmespath(path, node, key, parent, map_path, hash_func):
    def is_map_path(path, map_path):
        return match_wildcard(path, map_path)

    if not is_dict(node) and not is_list(node):
        return
    elif is_dict(node):
        for subkey in node.keys():
            _map_jmespath(f'{path}.{subkey}', node[subkey], subkey, node, map_path, hash_func)
    elif is_list(node) and (path == '@' or not match_wildcard(path, map_path)):
        for index, subnode in enumerate(node):
            _map_jmespath(f'{path}[{index}]', subnode, index, subnode, map_path, hash_func)
    elif is_list(node) and match_wildcard(path, map_path):
            parent[key] = {hash_func(subnode):subnode for subnode in node}
            return

def time_tick(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'{func.__name__}: {end_time - start_time}')
        return result

    return wrapper

def get_jmespath(json_obj, skip_paths=None):
    skip_paths = [] if skip_paths is None else skip_paths
    return _get_jmespath('@', json_obj, skip_paths)

def _get_jmespath(path, node, skip_paths):
    for skip_path in skip_paths:
        if match_wildcard(path, skip_path):
            return []

    if not is_dict(node) and not is_list(node):
        return [path]
    elif is_dict(node):
        temp = [path]
        for subkey in node.keys():
            temp += _get_jmespath(f"{path}.{subkey}", node[subkey], skip_paths)
        return temp
    elif is_list(node):
        temp = [path]
        for index, sub_node in enumerate(node):
            temp += _get_jmespath(f"{path}[{index}]", sub_node, skip_paths)
        return temp

class CompareResult:
    def __init__(self, diff_fields, a_missing_fields, b_missing_fields):
        self.diff_fields = diff_fields
        self.a_missing_fields = a_missing_fields
        self.b_missing_fields = b_missing_fields


def compare(a_json, b_json, skip_paths=None):
    skip_paths = [] if skip_paths is None else skip_paths
    return _compare(a_json, b_json, skip_paths)

def _compare(a_json, b_json, skip_paths):
    a_jmespath = set(get_jmespath(a_json, skip_paths))
    b_jmespath = set(get_jmespath(b_json, skip_paths))

    a_missing = b_jmespath - a_jmespath
    b_missing = a_jmespath - b_jmespath
    both_has = a_jmespath & b_jmespath

    diff_fields = []
    for path in both_has:
        a = jmespath.search(path, a_json)
        b = jmespath.search(path, b_json)

        if type(a) != type(b):
            reason = f'path:{path} is different, a_type:{type(a)} b_type:{type(b)}'
            diff_fields.append((path, a, b, reason))
        elif type(a) == dict and type(b) == dict:
            continue
        elif type(a) == list and type(b) == list:
            continue
        elif a != b:
            reason = f'path:{path} is different, a_value:{a} b_value:{b}'
            diff_fields.append((path, a, b, reason))

    a_missing_fields = []
    for path in a_missing:
        b = jmespath.search(path, b_json)
        a_missing_fields.append((path,b))

    b_missing_fields = []
    for path in b_missing:
        a = jmespath.search(path, a_json)
        b_missing_fields.append((path, a))

    diff_fields.sort(key=lambda item: item[0])
    a_missing_fields.sort(key=lambda item: item[0])
    b_missing_fields.sort(key=lambda item: item[0])

    return CompareResult(diff_fields, a_missing_fields, b_missing_fields)
