from wink.api.base import api
from wink.models.meta import WinkMeta
from wink.models.field import WinkField
from wink.common.resp import Success, NotFoundError, List
from wink.models.base import db
from wink.common import db_utils, meta_utils

from flask import request
from flask_login import current_user, login_required


@api.get('/meta/all')
@login_required
def meta_all():
    metas = WinkMeta.query.all()
    return Success(data=metas)


@api.get('/meta/list')
@login_required
def meta_list():
    metas = WinkMeta.query.all()
    return List(len(metas), metas, 1)


@api.post('/meta/add')
@login_required
def meta_add():
    # 获取 json 数据
    data = request.get_json()
    # TODO 表单验证
    meta = WinkMeta.query.filter_by(name=data['name']).first()
    if meta:
        return NotFoundError('meta 已存在')
    meta = WinkMeta(
        code=data['code'],
        name=data['name'],
        table=data['table'],
        pk=data['pk'],
        source=data['source'],
    )

    db.session.add(meta)
    db.session.commit()
    return Success()


@api.post('/meta/edit')
@login_required
def meta_edit():
    # 获取 json 数据
    data = request.get_json()
    # TODO 表单验证
    meta = WinkMeta.query.filter_by(id=data['id']).first()
    if not meta:
        return NotFoundError('meta 不存在')
    meta.code = data['code']
    meta.name = data['name']
    meta.table = data['table']
    meta.pk = data['pk']
    meta.source = data['source']
    db.session.commit()
    return Success()


@api.post('/meta/delete')
@login_required
def meta_delete():
    # 获取 json 数据
    data = request.get_json()
    meta = WinkMeta.query.filter_by(id=data['id']).first()
    if not meta:
        return NotFoundError('meta 不存在')
    db.session.delete(meta)
    db.session.commit()
    return Success()


@api.post('/meta/delete_many')
@login_required
def meta_delete_many():
    # 获取 json 数据
    data = request.get_json()
    ids = data['ids']
    metas = WinkMeta.query.filter(WinkMeta.id.in_(ids)).all()
    if not metas:
        return NotFoundError('meta 不存在')
    for meta in metas:
        db.session.delete(meta)
    db.session.commit()
    return Success()


@api.post('/meta/add_meta')
@login_required
def meta_add_meta():
    # 获取 json 数据
    data = request.get_json()
    # TODO 表单验证
    meta_utils.add_meta(data)
    return Success()


@api.post('/meta/add_record/<meta_code>')
@login_required
def meta_add_record(meta_code):
    # 保存 meta 记录
    data = request.get_json()
    # TODO 表单验证
    meta_utils.add_meta_record(meta_code, data)
    return Success()
