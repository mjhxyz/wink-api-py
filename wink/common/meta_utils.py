from wink.api.base import api
from wink.models.meta import WinkMeta
from wink.models.mapping import WinkMapping
from wink.models.field import WinkField
from wink.common.resp import NotFoundError
from wink.models.base import db
from wink.common import db_utils

from sqlalchemy import Column, Integer, String, Text, Float, Date, DateTime
from sqlalchemy.dialects.mysql import TINYINT

COMPO_MAPPING = {
    String: '文本框',
    Text: '文本域',
    Float: '浮点框',
    Date: '日期框',
    DateTime: '日期时间框',
}


def _generate_field_compo(field, field_dict):
    # 获取字段所用组件
    type_obj = field['type_obj']
    sqlalchemy_type = type_obj

    for k, v in COMPO_MAPPING.items():
        if isinstance(sqlalchemy_type, k):
            field_dict['compo'] = v
            return

    # 特殊数据类型处理
    field_label, field_mappping = db_utils.parse_comment(field['comment'])
    if isinstance(sqlalchemy_type, Integer):
        if not field_mappping:
            field_dict['compo'] = '整数框'
            return
        field_dict['compo'] = '下拉框'
        meta_code = field_dict['meta_code']
        field_name = field_dict['name']
        for value, name in field_mappping.items():
            mapping = WinkMapping(
                value=value,
                name=name,
                meta_code=meta_code,
                field=field_name,
            )
            db.session.add(mapping)
        field_dict['exp'] = f'''select value ,name from wink_mapping where meta_code = '{meta_code}' and field = '{field_name}';meta'''


def add_meta(data):
    # 添加 Meta 数据
    code = data['code']
    if WinkMeta.query.filter_by(code=code).first():
        raise NotFoundError(f'meta [{code}] 已存在')

    pk = db_utils.get_primary_key(data['source'], data['table'])
    WinkField.query.filter_by(meta_code=code).delete()
    WinkMapping.query.filter_by(meta_code=code).delete()

    # 事务添加 meta 记录和字段记录
    try:
        # meta 记录
        meta = WinkMeta(
            code=data['code'],
            name=data['name'],
            table=data['table'],
            pk=pk,
            source=data['source'],
        )
        db.session.add(meta)
        db.session.flush()

        # 字段记录
        fields = db_utils.get_table_field_list(data['source'], data['table'])
        for field in fields:
            field_type = field['type']
            if '(' in field_type:
                field_type = field_type.split('(')[0]
            field_dict = {
                'meta_code': data['code'],
                'weight': 10,
                'name': field['name'],
                'type': field_type,
                'width': 100,
                'label': db_utils.get_field_label(field)
            }
            _generate_field_compo(field, field_dict)

            db.session.add(WinkField(**field_dict))
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise e
