from wink.api.base import api
from wink.common.resp import Success


@api.post('/user/login')
def login():
    return Success({'token': '123456'})


@api.get('/user/logout')
def logout():
    return '登出!!!'


@api.get('/user/info')
def info():
    return Success({
        'roles': ['admin'],
        'introduction': 'I am a super administrator',
        'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        'name': 'Super Admin'
    })
