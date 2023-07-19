from sqlalchemy import Column, Integer, String

from wink.models.base import Base


class WinkMapping(Base):

    __tablename__ = 'wink_mapping'

    id = Column(Integer, primary_key=True, comment='字段ID', autoincrement=True)
    value = Column(String(50), nullable=False, comment='值')
    name = Column(String(50), nullable=False, comment='名称')
    meta_code = Column(String(50), nullable=False, comment='Meta code')
    field = Column(String(50), nullable=False, comment='字段名称')
