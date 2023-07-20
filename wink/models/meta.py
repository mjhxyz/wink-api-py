from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

from wink.models.base import Base


class WinkMeta(Base):

    __tablename__ = 'wink_meta'

    id = Column(Integer, primary_key=True, comment='Meta ID', autoincrement=True)
    code = Column(String(100), unique=True, nullable=False, comment='编码')
    name = Column(String(100), nullable=False, comment='名称')
    table = Column(String(100), nullable=False, comment='映射数据表名')
    pk = Column(String(100), nullable=False, comment='Meta映射的表的主键名')
    source = Column(String(100), nullable=False, comment='数据源')
