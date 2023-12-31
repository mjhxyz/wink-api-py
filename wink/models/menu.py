from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

from wink.models.base import Base


class WinkMenu(Base):

    __tablename__ = 'wink_menu'

    id = Column(Integer, primary_key=True, comment='菜单ID', autoincrement=True)
    code = Column(String(100), unique=True, nullable=False, comment='菜单编码')
    name = Column(String(100), nullable=False, comment='菜单名称')
    type = Column(String(100), nullable=False,
                  comment='菜单类型: dir=目录')
    weight = Column(Integer, nullable=False, comment='菜单权重', default=10)
    parent_id = Column(Integer, nullable=False,
                       comment='父级菜单ID', default=0)
    setting = Column(String(2000), nullable=False, comment='菜单配置')
    status = Column(Integer, nullable=False,
                    comment='状态: 1=正常, 0=禁用', default=1)
    bi_hook = Column(String(255), nullable=False, comment='业务钩子')

    # 虚拟字段
    children = []
