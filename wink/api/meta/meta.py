from wink.api.base import api
from wink.models.meta import WinkMeta
from wink.models.field import WinkField
from wink.common.resp import Success, NotFoundError, List
from wink.models.base import db
from wink.common import db_utils

from flask import request
from flask_login import current_user, login_required


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
    meta = WinkMeta.query.filter_by(name=data['name']).first()
    if meta:
        return NotFoundError('meta 已存在')
    # 获取所有字段
    fields = db_utils.get_table_field_list(data['source'], data['table'])
    # 获取主键
    pk = db_utils.get_primary_key(data['source'], data['table'])
    print(fields)
    # 事务添加 meta 记录和字段记录
    try:
        meta = WinkMeta(
            code=data['code'],
            name=data['name'],
            table=data['table'],
            pk=pk,
            source=data['source'],
        )
        db.session.add(meta)
        db.session.flush()
        for field in fields:
            db.session.add(WinkField(
                meta_code=data['code'],
                weight=10,
                name=field['name'],
                label=field['comment'] or field['name'],
                type=field['type'],
                width=100,
            ))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return Success(fields)
