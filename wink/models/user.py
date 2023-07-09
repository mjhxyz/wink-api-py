from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

from wink.models.base import Base


class WinkUser(Base):
    __tablename__ = 'wink_user'

    id = Column(Integer, primary_key=True, comment='用户ID')
    login_id = Column(String(24), unique=True, nullable=False, comment='登录ID')
    name = Column(String(24), nullable=False, comment='用户昵称')
    rid = Column(Integer, nullable=False, comment='角色ID')
    status = Column(Integer, nullable=False, comment='状态, 1=正常, 2=禁用')

    # 定义一个 _login_pwd 属性, 用于存储密码
    # 使用 @property 装饰器, _login_pwd 成为属性
    # 这样设置 _login_pwd 属性的时候，就可以先加密再赋值给 _login_pwd
    _login_pwd = Column('login_pwd', String(
        128), nullable=True, comment='登录密码')

    @property
    def login_pwd(self):
        return self._login_pwd

    @login_pwd.setter
    def login_pwd(self, raw_pwd):
        self._login_pwd = generate_password_hash(raw_pwd)

    def check_login_pwd(self, raw_pwd):
        return check_password_hash(self._login_pwd, raw_pwd)
