from wink.api.base import api
from wink.models.user import WinkUser
from wink.common.resp import Success, NotFoundError


@api.get('/user/list')
def list():
    users = WinkUser.query.all()
    return Success(users)
