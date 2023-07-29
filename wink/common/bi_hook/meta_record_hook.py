# 新增删除修改 hook
from wink.common.bi_hook.hook import register_hook, hook, dispatch, HookContext, ActionEnum


@hook('wink_bi_hook_menu_view')
def menu_view_hook(context: HookContext):
    path = context.path
    data = context.data
    action = context.action
    menu_code = context.menu_code
    meta_code = context.meta_code

    print(path, data, action, menu_code, meta_code)
    if action == ActionEnum.ADD:
        print('新增操作')
    elif action == ActionEnum.EDIT:
        print('修改操作')
    elif action == ActionEnum.DELETE:
        print('删除操作')
    elif action == ActionEnum.QUERY:
        print('查询操作')
