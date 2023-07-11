from wink.common.error import APIException


def Success(data=None):
    return APIException.ok(data).to_dict()


class Base(APIException):
    error_code = 1000
    data = None
    message = '成功'

    def __init__(self, message=None):
        if message is not None:
            self.message = message
        super().__init__(self.error_code, self.message, self.data)


def List(total, items, page):
    return APIException.ok({
        'total': total,
        'items': items,
        'page': page
    }).to_dict()


class TokenError(Base):
    error_code = 2002
    data = None
    message = 'Token错误'


class LoginError(Base):
    error_code = 2004
    data = None
    message = '用户名或密码错误'


class NotFoundError(Base):
    error_code = 2005
    data = None
    message = '资源未找到'


class ClientError(Base):
    error_code = 2006
    data = None
    message = '资源已存在'


class ServerError(Base):
    error_code = 3000
    data = None
    message = '服务器内部错误'
