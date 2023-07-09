from wink.api.base import api


@api.get('/login')
def login():
    return '登录!!!'


@api.get('/logout')
def logout():
    return '登出!!!'


@api.get('/info')
def info():
    return '用户信息!!!'
