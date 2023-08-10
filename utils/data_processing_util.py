import re
import jwt
import json
import random

from typing import Tuple, Any, Callable, Optional, Union, List


def safe_nested_get_value_in_dict(path: list, key: str, data: dict) -> Tuple[Any, str]:
    path = list(filter(
        lambda x: x,
        path
    ))
    if not path and key:
        val = data.get(key)
        if isinstance(val, list):
            return val, 'list'
        return val, 'dict'
    if not key or not path:
        return None, ''
    result = data
    for k in path:
        result = result.get(k, None) or None
        if not isinstance(result, dict):
            break
    if isinstance(result, list):
        return [
            r.get(key) if isinstance(r, dict) else None
            for r in result
        ], 'list'
    elif isinstance(result, dict):
        return result.get(key), 'dict'
    return None, ''


def add_field_in_source_dict(field_name: str, source_dict: dict, mode='dict'):
    if mode == 'dict':
        if field_name not in source_dict:
            source_dict[field_name] = {}
    elif mode == 'list':
        if field_name not in source_dict:
            source_dict[field_name] = []


# 打平任意的list
def drew_list(_source_list):
    single_list = []

    def parse_list(source_list):
        if isinstance(source_list, list):
            for item in source_list:
                parse_list(item)
        else:
            single_list.append(source_list)
    parse_list(_source_list)
    return single_list


def get_value_from_list_until_not_empty(source: list):
    for s in source:
        if s:
            return s


def bulk_remove_dict_key(key_set: list, source_dict: dict):
    for key in key_set:
        source_dict.pop(key, None)


def text_to_file_tuple(url, data):
    if re.search(r'(ihr\.zhaopin|lagou|search\.maimai)(?=\.(com|cn))', url.lower()):
        data_type = 'application/json'
    else:
        data_type = 'text/plain'

    return 'resume', data, data_type


# 自动补全array, 保证数据有序
def append_data_automatic_completion_to_list_by_count(source_list: list, count: int, value: Any, placeholder=None):
    while len(source_list) < (count - 1):
        source_list.append(placeholder)
    source_list.append(value)


# 将所有的"Object of type datetime is not JSON serializable" 直接转换掉
def format_dict_to_be_json_serializable(source: dict):
    def extract_list_data(source_list: list):
        for index, v in enumerate(source_list):
            if isinstance(v, dict):
                format_dict_to_be_json_serializable(v)
            elif isinstance(v, list):
                extract_list_data(v)
            else:
                try:
                    json.dumps(v)
                except TypeError as _e1:
                    source_list[index] = str(v)

    if source is None:
        return

    for key, value in source.items():
        if isinstance(value, list):
            extract_list_data(value)
        elif isinstance(value, dict):
            format_dict_to_be_json_serializable(value)
        else:
            if value is None:
                continue
            try:
                json.dumps(value)
            except TypeError as _e:
                source[key] = str(value)


def format_list_to_be_json_serializable(source: List[dict]):
    for s in source:
        format_dict_to_be_json_serializable(s)


def safe_get_nested_dict_value(source: dict, key_list: list):
    if not key_list:
        return
    result = source
    for key in key_list:
        result = result.get(key) or {}
    return result or None


def nested_reformat_json_str_to_dict(source: dict):
    for key, value in source.items():
        try:
            _v = json.loads(value)
        except (json.JSONDecodeError, TypeError) as _e:
            continue
        source[key] = _v


# 根据条件过滤掉dict中value为空的数据
def filter_empty_key_in_dict(source: dict, func: Optional[Callable] = None):
    return {
        i: source[i] for i in filter(lambda x: source[x] if not func else func, source)
    }


# 我tm吐了 pyjwt 和 jwt 这两个库居然是一样的import???
def decode_jwt_v2(jwt_str: str, secret: Optional[str] = None):
    try:
        verify = bool(secret)
        return jwt.PyJWT().decode(jwt_str, key=secret or "", options=dict(verify=verify, verify_signature=verify))
    except Exception as _e:
        return


def decode_jwt(jwt_str: str, secret: Optional[str] = None, field: Optional[str] = None) -> Optional[Union[dict, str]]:
    try:
        decode_result = jwt.decode(jwt_str, key=secret or "", verify=bool(secret))
    except Exception as _e:
        decode_result = decode_jwt_v2(jwt_str, secret)
    if field is None or decode_result is None:
        return decode_result
    return decode_result.get(field)


def parse_bool_args(source: Any):
    if source in ["false", "no", "0"]:
        return False
    return bool(source)


def cut_list(source: list, num: int):
    """
    切割数组变成二维数组, 以num为单位切
    :param source: 源数组
    :param num: 切割单位
    :return: List[list]
    """
    if not source:
        return []
    result = []
    index_list = list(range(0, len(source) + num, num))
    start = index_list[0]
    for idx in index_list[1:]:
        result.append(source[start:idx])
        start = idx
    return result


def get_random_color_code():
    colors = [hex(random.randint(16, 255)).replace("0x", "").upper() for _ in range(3)]
    return "#{}".format("".join(colors))


if __name__ == '__main__':
    d = {'a': {'e': [{'k': 10}, {'c': 100, 'e': None}]}, 'g': None}
    format_dict_to_be_json_serializable(d)
    print(safe_nested_get_value_in_dict(['a', 'b'], '', d))
    print(d)
    k = {"config": '{"a": "10"}', "tenant": "asd", "g": 1}
    nested_reformat_json_str_to_dict(k)
    print(k)
    print(filter_empty_key_in_dict({"a": 1, "b": None}))
    print(decode_jwt("eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VybmFtZTpzZGEiLCJ0ZW5hbnRJZCI6NDIsInRlbmFudEFsaWFzIjoi"
                     "bWFpc3VpbmVpeW9uZ3poYW9waW4tNDIiLCJleHAiOjE2NDgyMDMzMTk2NzUsInVzZXJJZCI6ImZiZTU0MDkxLWM4ZDctNGI"
                     "5NC1iYzgyLTg5MjkyYmI2Y2Q3OCIsImlhdCI6MTY0Njk5MzcxOTY3NX0.5J73yuzy_MJR2hv7bK_gLidtwykqROF_bE0O3S"
                     "5KGyo", field="userId"))
    print(cut_list(["1", "2", "10", "5"], 3))
    print(get_random_color_code())
