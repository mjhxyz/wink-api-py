from wink.api.base import api
from wink.models.user import WinkUser


@api.get('/user/list')
def list():
    users = WinkUser.query.all()
    print(users)
    return '用户列表!!!'
