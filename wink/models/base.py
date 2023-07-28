from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Base(db.Model):
    # 不会创建 base 表
    __abstract__ = True
    # status = Column(SmallInteger, default=1, comment='状态 1:正常 0:已删除')
    add_time = db.Column(db.DateTime, index=True, nullable=False,
                         default=datetime.now, comment='添加时间')
    update_time = db.Column(
        db.DateTime, index=True, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def set_attrs(self, attrs_dict):
        # 接受字典参数, 用于批量赋值
        # 从 wtforms 校验后 批量赋值
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
    # def delete(self):
    #     self.status = 0
