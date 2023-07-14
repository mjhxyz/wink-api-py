from wink.api.base import api
from wink.models.menu import WinkMenu
from wink.common.resp import Success, NotFoundError, List
from wink.models.base import db
from wink.api.views.menu import WinkMenuView

from flask import request
from flask_login import current_user, login_required


@api.get('/menu/list')
@login_required
def menu_list():
    menus = WinkMenu.query.all()
    return List(len(menus), menus, 1)


@api.post('/menu/add')
@login_required
def menu_add():
    # 获取 json 数据
    data = request.get_json()
    # TODO 表单验证
    menu = WinkMenu.query.filter_by(name=data['name']).first()
    if menu:
        return NotFoundError('菜单已存在')
    menu = WinkMenu(
        code=data['code'],
        name=data['name'],
        type=data['type'],
        weight=data['weight'],
        parent_id=data['parent_id'],
        setting=data['setting'],
    )

    db.session.add(menu)
    db.session.commit()
    return Success()


@api.post('/menu/edit')
@login_required
def menu_edit():
    # 获取 json 数据
    data = request.get_json()
    # TODO 表单验证
    menu = WinkMenu.query.filter_by(id=data['id']).first()
    if not menu:
        return NotFoundError('menu 不存在')
    menu.code = data['code']
    menu.name = data['name']
    menu.type = data['type']
    menu.weight = data['weight']
    menu.parent_id = data['parent_id']
    menu.setting = data['setting']
    db.session.commit()
    return Success()


@api.post('/menu/delete')
@login_required
def menu_delete():
    # 获取 json 数据
    data = request.get_json()
    # TODO 表单验证
    menu = WinkMenu.query.filter_by(id=data['id']).first()
    if not menu:
        return NotFoundError('menu 不存在')
    db.session.delete(menu)
    db.session.commit()
    return Success()


@api.post('/menu/delete_many')
@login_required
def menu_delete_many():
    # 获取 json 数据
    data = request.get_json()
    # TODO 表单验证
    menus = WinkMenu.query.filter(WinkMenu.id.in_(data['ids'])).all()
    if not menus:
        return NotFoundError('menu 不存在')
    for menu in menus:
        db.session.delete(menu)
    db.session.commit()
    return Success()


@api.get('/menu/tree')
@login_required
def menu_tree():
    menus = WinkMenu.query.all()
    # menu 的结构为 {parent_id: 1, id: 2, ....}
    # 先转换为 view
    # 返回树形结构 为 {id: 1, children: [{id: 2, children: []}]}

    # 1. 先转换为 view
    views = []
    for menu in menus:
        view = WinkMenuView(menu)
        views.append(view)

    # 2. 转换为树形结构, 从根节点开始, 可能有无限层
    tree = []
    for view in views:
        if view.parent_id == 0:
            tree.append(view)
        else:
            for parent in views:
                if view.parent_id == parent.id:
                    parent.children.append(view)
                    break

    return List(len(tree), tree, 1)
