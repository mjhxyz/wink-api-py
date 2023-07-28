# 权限按钮
from sqlalchemy import Column, Integer, String, Boolean

from wink.models.base import Base


class WinkButton(Base):
    __tablename__ = 'wink_button'

    id = Column(Integer, primary_key=True, comment='按钮ID', autoincrement=True)
    name = Column(String(100), nullable=False, comment='按钮名称')
    menu_code = Column(String(100), nullable=False, comment='菜单编码')
    icon = Column(String(255), comment='按钮图标')
    ui = Column(String(255), nullable=False, comment='按钮UI路径')
    bauth = Column(String(500), comment='按钮权限')
    order_num = Column(Integer, nullable=False, comment='按钮排序', default=30)
    is_hide = Column(Boolean, nullable=False,
                     comment='是否隐藏: 0=隐藏, 1=展示', default=False)
