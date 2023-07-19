from wink.api.base import api
from wink.models.meta import WinkMeta
from wink.models.field import WinkField
from wink.common.resp import NotFoundError
from wink.models.base import db
from wink.common import db_utils


def add_meta(data):
    # 添加 Meta 数据
    code = data['code']
    meta = WinkMeta.query.filter_by(code=code).first()
    if meta:
        raise NotFoundError(f'meta [{code}] 已存在')

    fields = db_utils.get_table_field_list(data['source'], data['table'])
    pk = db_utils.get_primary_key(data['source'], data['table'])
    WinkField.query.filter_by(meta_code=code).delete()

    # 事务添加 meta 记录和字段记录
