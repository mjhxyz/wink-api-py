# 业务狗子插件

# 钩子函数返回 None, 则继续执行
# 钩子函数返回 其他, 则直接响应
import contextlib
from enum import Enum
from functools import wraps

from flask import current_app, g, request


_hooks = {}


def bi_hook(key, menu_code, meta_code, action, data):
    if key not in _hooks:
        return None
    cur_hook = _hooks[key]
    path = request.path
    context = HookContext(path, action, menu_code, meta_code, data)
    result = cur_hook(context)
    if result is None:
        return None
    raise result


class ActionEnum(Enum):
    ADD = 'add'
    EDIT = 'edit'
    DELETE = 'delete'
    QUERY = 'query'

    @classmethod
    def from_str(cls, string):
        for name, action in cls.__members__.items():
            if action.value == string:
                return action
        raise Exception(f'业务钩子: 未知的 action: {string}')


class HookContext:
    def __init__(self, path, action, menu_code, meta_code, data):
        self.path = path  # 请求路径
        self.action = ActionEnum.from_str(action)  # 请求动作
        self.menu_code = menu_code
        self.meta_code = meta_code
        self.data = data  # 校验后的表单数据


def hook(key):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        _hooks[key] = wrapper
        return wrapper
    return decorator


def register_hook(key, func):
    if key in _hooks:
        raise Exception(f'业务钩子 [{key}] 已存在')
    _hooks[key] = func


def dispatch(key, *args, **kwargs):
    if key not in _hooks:
        return None
    return _hooks[key](*args, **kwargs)


def init_app(app):
    pass
