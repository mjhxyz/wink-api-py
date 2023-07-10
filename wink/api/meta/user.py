from wink.api.base import api
from wink.models.user import WinkUser
from wink.common.resp import Success, NotFoundError, List


@api.get('/user/list')
def user_list():
    users = WinkUser.query.all()
    return List(len(users), users, 1)
