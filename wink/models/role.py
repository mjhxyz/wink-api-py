from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

from wink.models.base import Base


class WinkRole(Base):
    __tablename__ = 'wink_role'

    id = Column(Integer, primary_key=True, comment='角色ID')
    name = Column(String(24), nullable=False, comment='角色名称')
    desc = Column(String(128), nullable=False, comment='角色描述')
