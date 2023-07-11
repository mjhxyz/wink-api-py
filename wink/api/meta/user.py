from wink.api.base import api
from wink.models.user import WinkUser
from wink.common.resp import Success, NotFoundError, List
from wink.models.base import db

from flask import request
from flask_login import current_user, login_required


@api.get('/user/list')
@login_required
def user_list():
    users = WinkUser.query.all()
    return List(len(users), users, 1)


@api.post('/user/add')
@login_required
def user_add():
    # 获取 json 数据
    data = request.get_json()
    # TODO 表单验证
    login_id = data['login_id']
    user = WinkUser.query.filter_by(login_id=login_id).first()
    if user:
        return NotFoundError('用户已存在')
    user = WinkUser(
        name=data['login_id'],
        rid=data['rid'],
        login_id=data['login_id'],
        login_pwd=data['login_pwd'],
        status=data['status'],
    )
    db.session.add(user)
    db.session.commit()
    return Success()


@api.post('/user/edit')
@login_required
def user_edit():
    # 获取 json 数据
    data = request.get_json()
    # TODO 表单验证
    user = WinkUser.query.filter_by(id=data['id']).first()
    if not user:
        return NotFoundError('用户不存在')
    user.name = data['login_id']
    user.rid = data['rid']
    user.login_id = data['login_id']
    user.status = data['status']
    db.session.commit()
    return Success()


@api.post('/user/delete')
@login_required
def user_delete():
    # 获取 json 数据
    data = request.get_json()
    # TODO 表单验证
    user = WinkUser.query.filter_by(id=data['id']).first()
    if not user:
        return NotFoundError('用户不存在')
    db.session.delete(user)
    db.session.commit()
    return Success()


@api.post('/user/delete_many')
@login_required
def user_delete_many():
    # 获取 json 数据
    data = request.get_json()
    # TODO 表单验证
    ids = data['ids']
    users = WinkUser.query.filter(WinkUser.id.in_(ids)).all()
    for user in users:
        db.session.delete(user)
    db.session.commit()
    return Success()
