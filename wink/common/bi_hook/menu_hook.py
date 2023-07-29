# 新增删除修改 hook
from wink.common.bi_hook.hook import register_hook, hook, dispatch, HookContext, ActionEnum
from wink.models.base import db
from wink.models.button import WinkButton

from flask import current_app


@hook('menu_hook')
def menu_view_hook(context: HookContext):
    path = context.path
    data = context.data
    action = context.action
    menu_code = context.menu_code
    meta_code = context.meta_code
    config = current_app.config

    print(path, data, action, menu_code, meta_code)
    if action == ActionEnum.ADD:
        # 顺便添加菜单的基础按钮
        buttons = config['BASIC_BUTTONS']
        menu_code = data.get('code')
        # 事务的方式添加
        for button in buttons:
            name = button['name']
            icon = button['icon']
            ui = button['ui']
            bauth = button['bauth']
            wink_button = WinkButton(
                name=name,
                icon=icon,
                ui=ui,
                bauth=bauth,
                menu_code=menu_code,
            )
            db.session.add(wink_button)
        try:
            db.session.commit()
        except Exception as e:
            # TODO 日志
            db.session.rollback()

    elif action == ActionEnum.EDIT:
        print('菜单的修改操作')
    elif action == ActionEnum.DELETE:
        print('菜单的删除操作')
    elif action == ActionEnum.QUERY:
        print('菜单的查询操作')
