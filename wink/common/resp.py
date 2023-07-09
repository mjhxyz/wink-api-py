from wink.common.error import APIException


def Success(data=None):
    return APIException.ok(data).to_dict()


class ServerError(APIException):
    error_code = 3000
    data = None
    message = '服务器内部错误'


class NotFoundError(APIException):
    error_code = 2005
    data = None
    message = '资源未找到'
