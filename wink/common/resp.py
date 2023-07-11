from wink.common.error import APIException


def Success(data=None):
    return APIException.ok(data).to_dict()


def List(total, items, page):
    return APIException.ok({
        'total': total,
        'items': items,
        'page': page
    }).to_dict()


class ServerError(APIException):
    error_code = 3000
    data = None
    message = '服务器内部错误'


class NotFoundError(APIException):
    error_code = 2005
    data = None
    message = '资源未找到'

    def __init__(self, message=None):
        if message is not None:
            self.message = message
        super().__init__(self.error_code, self.message, self.data)


class ClientError(APIException):
    error_code = 2006
    data = None
    message = '资源已存在'

    def __init__(self, message=None):
        if message is not None:
            self.message = message
        super().__init__(self.error_code, self.message, self.data)
