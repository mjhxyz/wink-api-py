from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import TINYINT
from werkzeug.security import generate_password_hash, check_password_hash

from wink.models.base import Base


class WinkField(Base):

    __tablename__ = 'wink_field'

    id = Column(Integer, primary_key=True, comment='字段ID', autoincrement=True)
    meta_code = Column(String(100), nullable=False, comment='Meta code')
    weight = Column(Integer, nullable=False, comment='字段权重, 越大越靠前')
    name = Column(String(100), nullable=False, comment='字段名称')
    label = Column(String(100), nullable=False, comment='字段中文名称')
    type = Column(String(255), nullable=False, comment='控件类型')
    exp = Column(String(800), nullable=True, comment='字段表达式')

    width = Column(Integer, nullable=False, comment='字段宽度', default=100)
    align = Column(String(6), nullable=False,
                   comment='字段对齐方式', default='left')
    placeholder = Column(String(100), nullable=False,
                         comment='字段占位符', default='')
    required = Column(TINYINT(1), nullable=False,
                      comment='是否必填, 1=是, 0=否', default=0)
    is_hide = Column(TINYINT(1), nullable=False,
                     comment='是否隐藏, 1=是, 0=否', default=0)

    # 以下是字段的校验
    max_length = Column(Integer, nullable=True, comment='最大长度')
    min_length = Column(Integer, nullable=True, comment='最小长度')
    default_value = Column(String(255), nullable=True, comment='默认值')
    is_editable = Column(TINYINT(1), nullable=False,
                         comment='是否可编辑, 1=是, 0=否', default=1)
    is_addable = Column(TINYINT(1), nullable=False,
                        comment='是否可新增, 1=是, 0=否', default=1)

    is_edit = Column(TINYINT(1), nullable=False,
                     comment='是否可编辑, 1=是, 0=否', default=1)
    is_add = Column(TINYINT(1), nullable=False,
                    comment='是否可新增, 1=是, 0=否', default=1)
    add_status = Column(Integer, nullable=False,
                        comment='新增状态, 0=正常, 1=只读, 2=隐藏, 3=禁用', default=0)
    edit_status = Column(Integer, nullable=False,
                         comment='编辑状态, 0=正常, 1=只读, 2=隐藏, 3=禁用', default=0)
